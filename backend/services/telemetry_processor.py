from datetime import datetime, timezone
import json
import logging
import threading
import time

from influxdb_client import Point

from backend.config.settings import settings
from backend.database.influx import InfluxDatabase
from backend.mqtt.client import MQTTClient
from backend.models.telemetry import Telemetry
from backend.services.device_event_service import DeviceEventService
from backend.alarms.alarm_engine import AlarmEngine


logger = logging.getLogger("industrial_iot")


class TelemetryProcessor:

    def __init__(self):
        self.db = InfluxDatabase()
        self.mqtt = MQTTClient()
        self.device_events = DeviceEventService()

        self.alarm_engine = AlarmEngine(
            self.db.write_api,
            settings.INFLUX_BUCKET,
            settings.INFLUX_ORG
        )

        self.running = False

        self.mqtt.client.on_message = self.on_message

    def on_message(self, client, userdata, message):

        topic = message.topic

        try:
            payload = message.payload.decode("utf-8")
            data = json.loads(payload)
        except Exception as exc:
            logger.error(
                "MQTT MESSAGE PARSE ERROR | topic=%s | error=%s",
                topic,
                exc
            )
            return

        if topic == settings.MQTT_STATUS_TOPIC:
            self.process_status(data)
            return

        if topic == settings.MQTT_EVENTS_TOPIC:
            self.process_event(data)
            return

        if topic == settings.MQTT_TOPIC:
            self.process_telemetry(data)
            return

        logger.warning(
            "MQTT UNKNOWN TOPIC | topic=%s",
            topic
        )

    def process_status(self, data):

        device_id = data.get("device_id")
        status = data.get("status")
        reason = data.get("reason", "")

        if not device_id or not status:
            logger.warning(
                "INVALID DEVICE STATUS | payload=%s",
                data
            )
            return

        status = str(status).lower()

        if status not in ("online", "offline"):
            logger.warning(
                "UNKNOWN DEVICE STATUS | device=%s | status=%s",
                device_id,
                status
            )
            return

        changed = self.device_events.record_status(
            device_id,
            status,
            reason
        )

        if changed:
            logger.info(
                "DEVICE STATUS EVENT | device=%s | status=%s | reason=%s",
                device_id,
                status,
                reason
            )
        else:
            logger.info(
                "DEVICE STATUS UNCHANGED | device=%s | status=%s",
                device_id,
                status
            )

    def process_event(self, data):

        device_id = data.get("device_id")
        event_type = data.get("event_type")
        message_text = data.get("message", "")

        logger.info(
            "DEVICE EVENT RECEIVED | device=%s | type=%s | message=%s",
            device_id,
            event_type,
            message_text
        )

    def process_telemetry(self, data):

        try:
            telemetry = Telemetry(**data)
        except Exception as exc:
            logger.error(
                "INVALID TELEMETRY | error=%s | payload=%s",
                exc,
                data
            )
            return

        logger.info(
            "TELEMETRY RECEIVED | device=%s | people=%s | temp=%.1fC | humidity=%.1f%%",
            telemetry.device_id,
            telemetry.people,
            telemetry.temperature,
            telemetry.humidity
        )

        status_changed = self.device_events.record_status(
            telemetry.device_id,
            "online",
            "telemetry_received"
        )

        if status_changed:
            logger.info(
                "DEVICE STATUS EVENT | device=%s | status=online",
                telemetry.device_id
            )

        self._update_device_health(telemetry)

        alarms = self.alarm_engine.check(
            telemetry.device_id,
            telemetry.people,
            telemetry.temperature,
            telemetry.humidity
        )

        self._write_environment(telemetry)

        if alarms:
            logger.warning(
                "ACTIVE ALARMS: %s",
                len(alarms)
            )

        logger.info(
            "TELEMETRY STORED | device=%s",
            telemetry.device_id
        )

    def _write_environment(self, telemetry):

        point = (
            Point("environment")
            .tag("device_id", telemetry.device_id)
            .tag("site", "site01")
            .tag("zone", "zone01")
            .field("people", telemetry.people)
            .field("temperature", telemetry.temperature)
            .field("humidity", telemetry.humidity)
            .time(telemetry.timestamp)
        )

        self.db.write(point)

    def _update_device_health(self, telemetry):

        point = (
            Point("device_health")
            .tag("device_id", telemetry.device_id)
            .tag("site", "site01")
            .tag("zone", "zone01")
            .field("people", telemetry.people)
            .field("temperature", telemetry.temperature)
            .field("humidity", telemetry.humidity)
            .time(telemetry.timestamp)
        )

        self.db.write(point)

    def run(self):

        self.running = True

        logger.info(
            "Starting Industrial IoT MQTT Processor"
        )

        logger.info(
            "Topic: %s",
            settings.MQTT_TOPIC
        )

        self.mqtt.connect()

        self.mqtt.client.loop_forever()

    def stop(self):

        self.running = False

        try:
            self.mqtt.client.disconnect()
        except Exception:
            pass

        try:
            self.db.close()
        except Exception:
            pass


def main():

    logging.basicConfig(
        level=getattr(
            logging,
            settings.LOG_LEVEL.upper(),
            logging.INFO
        ),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    logger.info("=" * 60)
    logger.info("INITIALIZING INDUSTRIAL TELEMETRY PROCESSOR")
    logger.info("=" * 60)

    processor = TelemetryProcessor()

    try:
        processor.run()
    except KeyboardInterrupt:
        logger.info("Processor stopped by user")
    finally:
        processor.stop()


if __name__ == "__main__":
    main()
