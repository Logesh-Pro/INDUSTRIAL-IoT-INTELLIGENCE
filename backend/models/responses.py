from typing import Any

from pydantic import BaseModel


class APIResponse(BaseModel):
    status: str
    data: Any = None
    message: str | None = None


class HealthResponse(BaseModel):
    status: str
    database: str
    mqtt: str = "unknown"


class DeviceSummary(BaseModel):
    total_devices: int
    online_devices: int
    offline_devices: int
    total_people: int
