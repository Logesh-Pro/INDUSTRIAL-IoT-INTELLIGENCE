import logging

import paho.mqtt.client as mqtt

from backend.config.settings import settings

logger = logging.getLogger(__name__)


class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=settings.MQTT_CLIENT_ID
        )

        if settings.MQTT_USERNAME:
            self.client.username_pw_set(
                settings.MQTT_USERNAME,
                settings.MQTT_PASSWORD
            )

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            logger.info("MQTT connected")
            logger.info(
                "Broker: %s:%s",
                settings.MQTT_BROKER,
                settings.MQTT_PORT
            )

            subscriptions = [
                (settings.MQTT_TOPIC, 1),
                (settings.MQTT_STATUS_TOPIC, 1),
                (settings.MQTT_EVENTS_TOPIC, 1)
            ]

            result, mid = client.subscribe(subscriptions)

            if result == mqtt.MQTT_ERR_SUCCESS:
                for topic, qos in subscriptions:
                    logger.info(
                        "Subscribed: %s | QoS=%s",
                        topic,
                        qos
                    )
            else:
                logger.error(
                    "MQTT subscription failed: %s",
                    result
                )

        else:
            logger.error(
                "MQTT connection failed: %s",
                reason_code
            )

    def _on_disconnect(
        self,
        client,
        userdata,
        disconnect_flags,
        reason_code,
        properties
    ):
        logger.warning(
            "MQTT disconnected: %s",
            reason_code
        )

    def connect(self):
        logger.info("Connecting to MQTT broker...")

        self.client.connect(
            settings.MQTT_BROKER,
            settings.MQTT_PORT,
            keepalive=60
        )

    def start(self):
        self.connect()
        self.client.loop_forever()

    def publish_status(self, device_id, status, reason=""):
        payload = (
            '{"device_id":"'
            + device_id
            + '","status":"'
            + status
            + '","reason":"'
            + reason
            + '"}'
        )

        self.client.publish(
            settings.MQTT_STATUS_TOPIC,
            payload,
            qos=1,
            retain=True
        )

    def publish_event(self, device_id, event_type, message):
        payload = (
            '{"device_id":"'
            + device_id
            + '","event_type":"'
            + event_type
            + '","message":"'
            + message
            + '"}'
        )

        self.client.publish(
            settings.MQTT_EVENTS_TOPIC,
            payload,
            qos=1
        )
