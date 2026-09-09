import logging

from backend.mqtt.client import MQTTClient


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


if __name__ == "__main__":
    mqtt_client = MQTTClient()
    mqtt_client.start()