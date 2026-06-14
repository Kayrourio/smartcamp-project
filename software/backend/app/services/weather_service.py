from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.integrations import open_meteo
from app.schemas.weather import WeatherOut, RainGridOut, GridPoint

_current_cache: dict = {}
_grid_cache: dict = {}

VIÇOSA_CENTER = (-20.7546, -42.8825)
GRID_OFFSETS = [-0.05, 0.0, 0.05]


def build_grid_coords() -> list[tuple[float, float]]:
    lat0, lng0 = VIÇOSA_CENTER
    return [
        (round(lat0 + dlat, 4), round(lng0 + dlng, 4))
        for dlat in GRID_OFFSETS
        for dlng in GRID_OFFSETS
    ]


def _is_fresh(cache: dict) -> bool:
    expires = cache.get("expires_at")
    return expires is not None and datetime.now(timezone.utc) < expires


async def get_current() -> WeatherOut:
    if _is_fresh(_current_cache):
        return _current_cache["data"]

    lat, lng = VIÇOSA_CENTER
    data = await open_meteo.fetch_current(lat, lng)

    ttl = timedelta(minutes=settings.weather_cache_ttl_minutes)
    expires_at = datetime.now(timezone.utc) + ttl

    result = WeatherOut(
        source="Open-Meteo",
        location="Viçosa, MG",
        rainfall_mm=data["rainfall_mm"],
        temperature_c=data["temperature_c"],
        humidity_pct=data["humidity_pct"],
        cached_until=expires_at.isoformat(),
    )
    _current_cache["data"] = result
    _current_cache["expires_at"] = expires_at
    return result


async def get_rain_grid() -> RainGridOut:
    if _is_fresh(_grid_cache):
        return _grid_cache["data"]

    coords = build_grid_coords()
    points = await open_meteo.fetch_grid(coords)

    ttl = timedelta(minutes=settings.weather_rain_grid_ttl_minutes)
    expires_at = datetime.now(timezone.utc) + ttl

    result = RainGridOut(
        source="Open-Meteo",
        resolution_km=1,
        cached_until=expires_at.isoformat(),
        grid=[GridPoint(lat=p["lat"], lng=p["lng"], rainfall_mm=p["rainfall_mm"]) for p in points],
    )
    _grid_cache["data"] = result
    _grid_cache["expires_at"] = expires_at
    return result
