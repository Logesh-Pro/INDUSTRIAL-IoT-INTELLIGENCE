from datetime import datetime, timezone

from backend.config.settings import settings
from backend.database.influx import InfluxDatabase


class DeviceService:
    def __init__(self):
        self.db = InfluxDatabase()

    def get_devices(self, minutes=10):
        query = f'''
        from(bucket: "telemetry")
          |> range(start: -{minutes}m)
          |> filter(fn: (r) => r["_measurement"] == "device_health")
          |> group(columns: ["device_id", "_field"])
          |> last()
        '''

        tables = self.db.query(query)
        devices = {}

        for table in tables:
            for record in table.records:
                device_id = record.values.get("device_id")

                if device_id not in devices:
                    devices[device_id] = {
                        "device_id": device_id,
                        "status": "online"
                    }

                devices[device_id][record.get_field()] = record.get_value()

                if record.get_time():
                    devices[device_id]["last_seen"] = record.get_time().isoformat()

        for device in devices.values():
            last_seen = device.get("last_seen")

            if not last_seen:
                device["status"] = "unknown"
                device["online"] = 0
                continue

            timestamp = datetime.fromisoformat(last_seen)

            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)

            age = (
                datetime.now(timezone.utc) - timestamp
            ).total_seconds()

            device["seconds_since_last_seen"] = round(age, 1)

            device["offline_timeout_seconds"] = (
                settings.DEVICE_OFFLINE_TIMEOUT_SECONDS
            )

            if age > settings.DEVICE_OFFLINE_TIMEOUT_SECONDS:
                device["status"] = "offline"
                device["online"] = 0
            else:
                device["status"] = "online"
                device["online"] = 1

        return list(devices.values())

    def get_device(self, device_id):
        devices = self.get_devices()

        for device in devices:
            if device["device_id"] == device_id:
                return device

        return None

    def close(self):
        self.db.close()
