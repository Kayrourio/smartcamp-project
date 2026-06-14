from pydantic import BaseModel


class EpdReadingIn(BaseModel):
    epd_uid: str
    soil_moisture: float
    rainfall: float | None = None
    temperature: float | None = None
    angle_x: float | None = None
    angle_y: float | None = None
    angle_z: float | None = None


class CpdBatchIn(BaseModel):
    cpd_uid: str
    readings: list[EpdReadingIn]


class CpdBatchOut(BaseModel):
    received: int
    skipped: int
    timestamp: str
