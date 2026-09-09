from datetime import datetime, timezone

from influxdb_client import Point


class AlarmEngine:

    THRESHOLDS = {
        "HIGH_TEMPERATURE": {
            "field": "temperature",
            "threshold": 32.0,
            "severity": "CRITICAL"
        },
        "HIGH_OCCUPANCY": {
            "field": "people",
            "threshold": 7,
            "severity": "WARNING"
        },
        "HIGH_HUMIDITY": {
            "field": "humidity",
            "threshold": 80.0,
            "severity": "WARNING"
        }
    }

    def __init__(self, write_api, bucket, org):
        self.write_api = write_api
        self.bucket = bucket
        self.org = org

        # Runtime alarm state.
        # Key = (device_id, alarm_type)
        self.active_alarms = {}

    def _value_for_alarm(self, alarm_type, people, temperature, humidity):
        field = self.THRESHOLDS[alarm_type]["field"]

        if field == "temperature":
            return float(temperature)

        if field == "people":
            return int(people)

        if field == "humidity":
            return float(humidity)

        return 0

    def _write_event(
        self,
        device_id,
        alarm_type,
        severity,
        status,
        value,
        message
    ):
        point = (
            Point("alarms")
            .tag("device_id", device_id)
            .tag("alarm_type", alarm_type)
            .tag("severity", severity)
            .tag("status", status)
            .field("value", float(value))
            .field("message", message)
            .time(datetime.now(timezone.utc))
        )

        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=point
        )

    def check(
        self,
        device_id,
        people,
        temperature,
        humidity
    ):
        current = []

        for alarm_type, config in self.THRESHOLDS.items():

            value = self._value_for_alarm(
                alarm_type,
                people,
                temperature,
                humidity
            )

            threshold = config["threshold"]
            severity = config["severity"]

            is_active = value >= threshold
            key = (device_id, alarm_type)
            was_active = key in self.active_alarms

            if is_active:

                alarm = {
                    "device_id": device_id,
                    "alarm_type": alarm_type,
                    "severity": severity,
                    "status": "ACTIVE",
                    "value": value,
                    "message": self._active_message(
                        alarm_type,
                        value
                    )
                }

                current.append(alarm)

                if not was_active:
                    self._write_event(
                        device_id,
                        alarm_type,
                        severity,
                        "ACTIVE",
                        value,
                        alarm["message"]
                    )

                    self.active_alarms[key] = alarm

            else:

                if was_active:

                    self._write_event(
                        device_id,
                        alarm_type,
                        severity,
                        "CLEARED",
                        value,
                        f"{alarm_type} condition cleared"
                    )

                    del self.active_alarms[key]

        return current

    def _active_message(self, alarm_type, value):

        if alarm_type == "HIGH_TEMPERATURE":
            return f"Temperature is {value:.1f}C"

        if alarm_type == "HIGH_OCCUPANCY":
            return f"Occupancy is {int(value)} people"

        if alarm_type == "HIGH_HUMIDITY":
            return f"Humidity is {value:.1f}%"

        return f"{alarm_type} condition active"

    def get_active_alarms(self):
        return list(self.active_alarms.values())
