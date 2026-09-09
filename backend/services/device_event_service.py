from datetime import datetime, timezone

from influxdb_client import Point

from backend.config.settings import settings
from backend.database.influx import InfluxDatabase


class DeviceEventService:

    def __init__(self):
        self.db = InfluxDatabase()
        self.last_status = {}

    def record_status(self, device_id, status, reason=""):
        previous = self.last_status.get(device_id)

        if previous == status:
            return False

        point = (
            Point("device_events")
            .tag("device_id", device_id)
            .tag("site", "site01")
            .tag("zone", "zone01")
            .tag("status", status)
            .field("reason", reason)
            .time(datetime.now(timezone.utc))
        )

        self.db.write(point)

        self.last_status[device_id] = status

        return True

    def get_events(self, hours=24):
        query = f'''
        from(bucket: "{settings.INFLUX_BUCKET}")
          |> range(start: -{hours}h)
          |> filter(fn: (r) => r["_measurement"] == "device_events")
          |> sort(columns: ["_time"], desc: true)
        '''

        tables = self.db.query(query)
        results = []

        for table in tables:
            for record in table.records:
                results.append({
                    "timestamp": record.get_time().isoformat(),
                    "device_id": record.values.get("device_id"),
                    "site": record.values.get("site"),
                    "zone": record.values.get("zone"),
                    "status": record.values.get("status"),
                    "field": record.get_field(),
                    "value": record.get_value()
                })

        return results

    def close(self):
        self.db.close()
