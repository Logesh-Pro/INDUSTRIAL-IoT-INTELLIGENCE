from backend.database.influx import InfluxDatabase
from backend.config.settings import settings

class EventService:
    def __init__(self):
        self.db = InfluxDatabase()

    def get_history(self, hours=24):
        query = f'''
        from(bucket: "{settings.INFLUX_BUCKET}")
          |> range(start: -{hours}h)
          |> filter(fn: (r) => r["_measurement"] == "environment")
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
                    "field": record.get_field(),
                    "value": record.get_value()
                })

        return results

    def get_alarms(self, hours=24):
        query = f'''
        from(bucket: "{settings.INFLUX_BUCKET}")
          |> range(start: -{hours}h)
          |> filter(fn: (r) => r["_measurement"] == "alarms")
          |> sort(columns: ["_time"], desc: true)
        '''

        tables = self.db.query(query)

        grouped = {}

        for table in tables:
            for record in table.records:
                timestamp = record.get_time().isoformat()
                device_id = record.values.get("device_id")
                alarm_type = record.values.get("alarm_type")
                severity = record.values.get("severity")
                status = record.values.get("status")
                field = record.get_field()
                value = record.get_value()

                key = (
                    timestamp,
                    device_id,
                    alarm_type,
                    severity,
                    status
                )

                if key not in grouped:
                    grouped[key] = {
                        "timestamp": timestamp,
                        "device_id": device_id,
                        "alarm_type": alarm_type,
                        "severity": severity,
                        "status": status
                    }

                if field == "value":
                    grouped[key]["value"] = value

                if field == "message":
                    grouped[key]["message"] = value

        return sorted(
            grouped.values(),
            key=lambda x: x["timestamp"],
            reverse=True
        )

    def get_active_alarms(self):
        """
        Determine CURRENT active alarms from the latest telemetry.

        Historical alarm records are retained separately by get_alarms().
        This prevents an old ACTIVE event from remaining active forever
        after a processor restart.
        """

        query = f'''
        from(bucket: "{settings.INFLUX_BUCKET}")
          |> range(start: -24h)
          |> filter(fn: (r) => r["_measurement"] == "environment")
          |> filter(fn: (r) =>
              r["_field"] == "people" or
              r["_field"] == "temperature" or
              r["_field"] == "humidity"
          )
          |> group(columns: ["device_id", "_field"])
          |> last()
        '''

        tables = self.db.query(query)

        devices = {}

        for table in tables:
            for record in table.records:
                device_id = record.values.get("device_id")

                if not device_id:
                    continue

                if device_id not in devices:
                    devices[device_id] = {
                        "device_id": device_id
                    }

                field = record.get_field()

                devices[device_id][field] = record.get_value()

                if record.get_time():
                    devices[device_id]["timestamp"] = record.get_time().isoformat()

        alarms = []

        for device in devices.values():

            device_id = device["device_id"]

            temperature = device.get("temperature")
            people = device.get("people")
            humidity = device.get("humidity")

            timestamp = device.get("timestamp")

            if temperature is not None and temperature >= 32.0:
                alarms.append({
                    "alarm_type": "HIGH_TEMPERATURE",
                    "device_id": device_id,
                    "message": f"Temperature is {float(temperature):.1f}C",
                    "severity": "CRITICAL",
                    "status": "ACTIVE",
                    "timestamp": timestamp,
                    "value": float(temperature)
                })

            if people is not None and int(people) >= 7:
                alarms.append({
                    "alarm_type": "HIGH_OCCUPANCY",
                    "device_id": device_id,
                    "message": f"Occupancy is {int(people)} people",
                    "severity": "WARNING",
                    "status": "ACTIVE",
                    "timestamp": timestamp,
                    "value": int(people)
                })

            if humidity is not None and float(humidity) >= 80.0:
                alarms.append({
                    "alarm_type": "HIGH_HUMIDITY",
                    "device_id": device_id,
                    "message": f"Humidity is {float(humidity):.1f}%",
                    "severity": "WARNING",
                    "status": "ACTIVE",
                    "timestamp": timestamp,
                    "value": float(humidity)
                })

        return {
            "alarms": alarms,
            "count": len(alarms)
        }

    def get_active_alarms_from_latest(self):
        return self.get_active_alarms()

    def close(self):
        self.db.close()
