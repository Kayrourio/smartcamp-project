from pydantic import BaseModel


class WeatherOut(BaseModel):
    source: str
    location: str
    rainfall_mm: float
    temperature_c: float
    humidity_pct: float
    cached_until: str


class GridPoint(BaseModel):
    lat: float
    lng: float
    rainfall_mm: float


class RainGridOut(BaseModel):
    source: str
    resolution_km: int
    cached_until: str
    grid: list[GridPoint]
