from fastapi import APIRouter, HTTPException

from app.schemas.weather import WeatherOut, RainGridOut
from app.services import weather_service

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/current", response_model=WeatherOut)
async def current():
    try:
        return await weather_service.get_current()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Open-Meteo error: {exc}")


@router.get("/rain-grid", response_model=RainGridOut)
async def rain_grid():
    try:
        return await weather_service.get_rain_grid()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Open-Meteo error: {exc}")
