import serial
import json
import time
from datetime import datetime, timezone, timedelta
import paho.mqtt.client as mqtt

# ---------------- CONFIG ----------------
SERIAL_PORT = "COM3"
BAUD_RATE = 115200

MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883

MQTT_TOPIC = "industrial/site01/zone01/telemetry"

# ---------------- MQTT ----------------
client = mqtt.Client(client_id="ESP32_USB_BRIDGE")

print("Connecting to MQTT broker...")

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

print("MQTT connected")
print(f"Opening ESP32 serial port: {SERIAL_PORT}")

# ---------------- SERIAL ----------------
ser = serial.Serial(
    SERIAL_PORT,
    BAUD_RATE,
    timeout=1
)

time.sleep(2)

print("ESP32 USB connected")
print("----------------------------------------")
print("Waiting for telemetry...")
print("----------------------------------------")

# India Standard Time
INDIA_TZ = timezone(timedelta(hours=5, minutes=30))

while True:

    try:

        line = ser.readline().decode("utf-8", errors="ignore").strip()

        if not line:
            continue

        # We only process JSON telemetry lines
        if not line.startswith("{"):
            continue

        try:
            data = json.loads(line)

        except json.JSONDecodeError:
            continue

        # Make sure this is our ESP32 telemetry
        if data.get("device_id") != "ESP32_01":
            continue

        # Backend requires timestamp
        data["timestamp"] = datetime.now(INDIA_TZ).isoformat()

        # Convert data back to JSON
        payload = json.dumps(data)

        result = client.publish(
            MQTT_TOPIC,
            payload,
            qos=1
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:

            print(
                f"TELEMETRY → MQTT | "
                f"device={data['device_id']} | "
                f"people={data['people']} | "
                f"temp={data['temperature']}C | "
                f"humidity={data['humidity']}% | "
                f"timestamp={data['timestamp']}"
            )

        else:
            print("MQTT publish failed")

    except KeyboardInterrupt:

        print("\nStopping USB bridge...")
        break

    except serial.SerialException as e:

        print(f"Serial error: {e}")
        break

    except Exception as e:

        print(f"Error: {e}")

client.loop_stop()
client.disconnect()
ser.close()

print("USB bridge stopped")