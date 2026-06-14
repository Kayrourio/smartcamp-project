from datetime import datetime
from pydantic import BaseModel


class SensorReadingIn(BaseModel):
    sensor_id: str
    soil_moisture: float
    rainfall: float | None = None
    temperature: float | None = None
    lux: int | None = None


class SensorReadingOut(BaseModel):
    sensor_id: str
    location: str
    soil_moisture: float
    rainfall: float | None
    temperature: float | None
    lux: int | None
    risk_level: str
    timestamp: datetime
    online: bool

    model_config = {"from_attributes": True}


class HistoryPoint(BaseModel):
    soil_moisture: float
    timestamp: datetime


class SensorHistoryOut(BaseModel):
    sensor_id: str
    readings: list[HistoryPoint]
