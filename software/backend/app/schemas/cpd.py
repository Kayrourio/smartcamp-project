from pydantic import BaseModel


class EpdReadingIn(BaseModel):
    epd_uid: str
    soil_moisture: float
    rainfall: float | None = None
    temperature: float | None = None
    lux: int | None = None


class CpdBatchIn(BaseModel):
    cpd_uid: str
    readings: list[EpdReadingIn]


class CpdBatchOut(BaseModel):
    received: int
    skipped: int
    timestamp: str
