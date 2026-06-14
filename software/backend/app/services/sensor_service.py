from datetime import datetime, timedelta, timezone

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reading import SensorReading
from app.schemas.sensor import SensorReadingIn, SensorReadingOut, SensorHistoryOut, HistoryPoint

SENSOR_LOCATION = "Campus UFV · Viçosa, MG"
ONLINE_THRESHOLD_SECONDS = 30


def compute_risk(soil_moisture: float) -> str:
    if soil_moisture >= 80:
        return "CRITICAL"
    if soil_moisture >= 60:
        return "ATTENTION"
    return "SAFE"


async def save_reading(db: AsyncSession, payload: SensorReadingIn) -> SensorReading:
    row = SensorReading(
        sensor_id=payload.sensor_id,
        soil_moisture=payload.soil_moisture,
        rainfall=payload.rainfall,
        temperature=payload.temperature,
        lux=payload.lux,
        risk_level=compute_risk(payload.soil_moisture),
    )
    db.add(row)
    await db.commit()
    await db.refresh(row)
    return row


async def get_latest(db: AsyncSession, sensor_id: str = "EPD-01") -> SensorReadingOut | None:
    stmt = (
        select(SensorReading)
        .where(SensorReading.sensor_id == sensor_id)
        .order_by(desc(SensorReading.created_at))
        .limit(1)
    )
    result = await db.execute(stmt)
    row = result.scalar_one_or_none()
    if row is None:
        return None

    now = datetime.now(timezone.utc)
    age = (now - row.created_at.replace(tzinfo=timezone.utc)).total_seconds()

    return SensorReadingOut(
        sensor_id=row.sensor_id,
        location=SENSOR_LOCATION,
        soil_moisture=float(row.soil_moisture),
        rainfall=float(row.rainfall) if row.rainfall is not None else None,
        temperature=float(row.temperature) if row.temperature is not None else None,
        lux=row.lux,
        risk_level=row.risk_level,
        timestamp=row.created_at,
        online=age < ONLINE_THRESHOLD_SECONDS,
    )


async def get_history(db: AsyncSession, sensor_id: str = "EPD-01", minutes: int = 10) -> SensorHistoryOut:
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    stmt = (
        select(SensorReading)
        .where(
            SensorReading.sensor_id == sensor_id,
            SensorReading.created_at >= cutoff,
        )
        .order_by(SensorReading.created_at)
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return SensorHistoryOut(
        sensor_id=sensor_id,
        readings=[HistoryPoint(soil_moisture=float(r.soil_moisture), timestamp=r.created_at) for r in rows],
    )
