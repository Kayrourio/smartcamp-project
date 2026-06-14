from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.sensor import SensorReadingIn, SensorReadingOut, SensorHistoryOut
from app.services import sensor_service

router = APIRouter()


@router.post("/sensor/reading", response_model=SensorReadingOut, status_code=201)
async def ingest_reading(payload: SensorReadingIn, db: AsyncSession = Depends(get_db)):
    row = await sensor_service.save_reading(db, payload)
    return await sensor_service.get_latest(db, payload.sensor_id)


@router.get("/sensor/latest", response_model=SensorReadingOut)
async def latest(sensor_id: str = Query(default="EPD-01"), db: AsyncSession = Depends(get_db)):
    data = await sensor_service.get_latest(db, sensor_id)
    if data is None:
        # Return mock data when no real readings exist yet
        return SensorReadingOut(
            sensor_id=sensor_id,
            location="Campus UFV · Viçosa, MG",
            soil_moisture=42.0,
            rainfall=0.0,
            temperature=22.5,
            lux=4000,
            risk_level="SAFE",
            timestamp=datetime.now(timezone.utc),
            online=False,
        )
    return data


@router.get("/sensor/history", response_model=SensorHistoryOut)
async def history(
    sensor_id: str = Query(default="EPD-01"),
    minutes: int = Query(default=10, ge=1, le=1440),
    db: AsyncSession = Depends(get_db),
):
    return await sensor_service.get_history(db, sensor_id, minutes)
