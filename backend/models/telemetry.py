from datetime import datetime

from pydantic import BaseModel, Field


class Telemetry(BaseModel):
    device_id: str = Field(min_length=1)
    timestamp: datetime

    people: int = Field(ge=0)

    temperature: float = Field(
        ge=-40,
        le=125
    )

    humidity: float = Field(
        ge=0,
        le=100
    )