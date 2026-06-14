from datetime import datetime, timedelta, timezone

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.epd import Epd
from app.models.reading import SensorReading
from app.schemas.epd import EpdOut, ReadingOut, EpdHistoryOut


def _reading_out(row: SensorReading) -> ReadingOut:
    return ReadingOut(
        soil_moisture=float(row.soil_moisture),
        rainfall=float(row.rainfall) if row.rainfall is not None else None,
        temperature=float(row.temperature) if row.temperature is not None else None,
        lux=row.lux,
        risk_level=row.risk_level,
        received_at=row.received_at,
    )


async def get_all_with_latest(db: AsyncSession) -> list[EpdOut]:
    epd_stmt = select(Epd).where(Epd.active == True).order_by(Epd.id)
    result = await db.execute(epd_stmt)
    epds = result.scalars().all()

    out = []
    for epd in epds:
        latest_stmt = (
            select(SensorReading)
            .where(SensorReading.epd_id == epd.id)
            .order_by(desc(SensorReading.received_at))
            .limit(1)
        )
        latest_result = await db.execute(latest_stmt)
        latest_row = latest_result.scalar_one_or_none()

        out.append(
            EpdOut(
                epd_uid=epd.epd_uid,
                label=epd.label,
                lat=float(epd.lat) if epd.lat is not None else None,
                lng=float(epd.lng) if epd.lng is not None else None,
                active=epd.active,
                latest=_reading_out(latest_row) if latest_row else None,
            )
        )
    return out


async def get_history(db: AsyncSession, epd_uid: str, minutes: int) -> EpdHistoryOut:
    cutoff = datetime.now(timezone.utc) - timedelta(minutes=minutes)

    epd_stmt = select(Epd).where(Epd.epd_uid == epd_uid)
    epd_result = await db.execute(epd_stmt)
    epd = epd_result.scalar_one_or_none()

    if epd is None:
        return EpdHistoryOut(epd_uid=epd_uid, readings=[])

    stmt = (
        select(SensorReading)
        .where(
            SensorReading.epd_id == epd.id,
            SensorReading.received_at >= cutoff,
        )
        .order_by(SensorReading.received_at)
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()

    return EpdHistoryOut(
        epd_uid=epd_uid,
        readings=[_reading_out(r) for r in rows],
    )
