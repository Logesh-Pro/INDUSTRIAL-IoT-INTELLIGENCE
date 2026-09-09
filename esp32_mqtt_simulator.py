import json
import random
import signal
import sys
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

from backend.config.settings import settings


DEVICE_ID = "ESP32_01"

TELEMETRY_TOPIC = settings.MQTT_TOPIC
STATUS_TOPIC = settings.MQTT_STATUS_TOPIC
EVENTS_TOPIC = settings.MQTT_EVENTS_TOPIC

running = True


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def graceful_shutdown(signum=None, frame=None):
    global running
    running = False


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("=" * 60)
        print("ESP32 MQTT SIMULATOR")
        print("=" * 60)
        print("Device:", DEVICE_ID)
        print("Broker:", f"{settings.MQTT_BROKER}:{settings.MQTT_PORT}")
        print("Telemetry:", TELEMETRY_TOPIC)
        print("Status:", STATUS_TOPIC)
        print("Events:", EVENTS_TOPIC)
        print()

        online_payload = json.dumps({
            "device_id": DEVICE_ID,
            "status": "online",
            "reason": "mqtt_connected",
            "timestamp": timestamp()
        })

        client.publish(
            STATUS_TOPIC,
            online_payload,
            qos=1,
            retain=True
        )

        print("STATUS -> ONLINE")

    else:
        print("MQTT connection failed:", reason_code)


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print("MQTT disconnected:", reason_code)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"{DEVICE_ID}_simulator"
)

client.will_set(
    STATUS_TOPIC,
    json.dumps({
        "device_id": DEVICE_ID,
        "status": "offline",
        "reason": "unexpected_disconnect",
        "timestamp": timestamp()
    }),
    qos=1,
    retain=True
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect

signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)


print("Connecting to MQTT broker...")

client.connect(
    settings.MQTT_BROKER,
    settings.MQTT_PORT,
    keepalive=15
)

client.loop_start()

people = 3
temperature = 27.0
humidity = 60.0

try:
    while running:

        people += random.choice([-1, 0, 0, 1])
        people = max(0, min(10, people))

        temperature += random.uniform(-0.4, 0.4)
        temperature = max(24.0, min(36.0, temperature))

        humidity += random.uniform(-1.5, 1.5)
        humidity = max(40.0, min(90.0, humidity))

        payload = {
            "device_id": DEVICE_ID,
            "timestamp": timestamp(),
            "people": people,
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1)
        }

        result = client.publish(
            TELEMETRY_TOPIC,
            json.dumps(payload),
            qos=1
        )

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(
                f"TELEMETRY | people={people:2d} | "
                f"temp={temperature:4.1f}C | "
                f"humidity={humidity:4.1f}%"
            )
        else:
            print("Telemetry publish failed:", result.rc)

        time.sleep(2)

finally:

    if client.is_connected():

        offline_payload = json.dumps({
            "device_id": DEVICE_ID,
            "status": "offline",
            "reason": "graceful_shutdown",
            "timestamp": timestamp()
        })

        client.publish(
            STATUS_TOPIC,
            offline_payload,
            qos=1,
            retain=True
        )

        time.sleep(1)

    client.loop_stop()
    client.disconnect()

    print()
    print("Simulator stopped.")


sys.exit(0)
