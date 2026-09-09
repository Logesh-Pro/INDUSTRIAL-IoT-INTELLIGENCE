import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Settings:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    MQTT_BROKER = os.getenv("MQTT_BROKER", "127.0.0.1")
    MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
    MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
    MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")
    MQTT_TOPIC = os.getenv(
        "MQTT_TOPIC",
        "industrial/site01/zone01/telemetry"
    )
    MQTT_CLIENT_ID = os.getenv(
        "MQTT_CLIENT_ID",
        "iiot_backend"
    )
    MQTT_STATUS_TOPIC = os.getenv(
        "MQTT_STATUS_TOPIC",
        "industrial/site01/zone01/status"
    )
    MQTT_EVENTS_TOPIC = os.getenv(
        "MQTT_EVENTS_TOPIC",
        "industrial/site01/zone01/events"
    )

    INFLUX_URL = os.getenv(
        "INFLUX_URL",
        "http://localhost:8086"
    )
    INFLUX_TOKEN = os.getenv("INFLUX_TOKEN", "")
    INFLUX_ORG = os.getenv(
        "INFLUX_ORG",
        "industrial_iot"
    )
    INFLUX_BUCKET = os.getenv(
        "INFLUX_BUCKET",
        "telemetry"
    )

    API_HOST = os.getenv("API_HOST", "127.0.0.1")
    API_PORT = int(os.getenv("API_PORT", "5000"))

    DEVICE_OFFLINE_TIMEOUT_SECONDS = int(
        os.getenv("DEVICE_OFFLINE_TIMEOUT_SECONDS", "15")
    )
    DEVICE_HEALTH_CHECK_INTERVAL_SECONDS = int(
        os.getenv("DEVICE_HEALTH_CHECK_INTERVAL_SECONDS", "5")
    )


settings = Settings()
