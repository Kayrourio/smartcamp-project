from datetime import datetime
from pydantic import BaseModel


class ReadingOut(BaseModel):
    soil_moisture: float
    rainfall: float | None
    temperature: float | None
    lux: int | None
    risk_level: str
    received_at: datetime

    model_config = {"from_attributes": True}


class EpdOut(BaseModel):
    epd_uid: str
    label: str | None
    lat: float | None
    lng: float | None
    active: bool
    latest: ReadingOut | None

    model_config = {"from_attributes": True}


class EpdHistoryOut(BaseModel):
    epd_uid: str
    readings: list[ReadingOut]
