from datetime import datetime, timezone


class DeviceRegistry:

    def __init__(self):
        self.devices = {}

    def update(
        self,
        device_id,
        people,
        temperature,
        humidity
    ):
        self.devices[device_id] = {
            "device_id": device_id,
            "site": "site01",
            "zone": "zone01",
            "device_type": "ESP32",
            "status": "online",
            "last_seen": datetime.now(
                timezone.utc
            ).isoformat(),
            "people": people,
            "temperature": temperature,
            "humidity": humidity
        }

    def get_all(self):
        return list(self.devices.values())

    def get(self, device_id):
        return self.devices.get(device_id)

    def remove(self, device_id):
        return self.devices.pop(
            device_id,
            None
        )

    def count(self):
        return len(self.devices)
