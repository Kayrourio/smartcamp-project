from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.epd import Epd
from app.models.reading import SensorReading
from app.schemas.cpd import CpdBatchIn

RISK_THRESHOLDS = {
    "CRITICAL": 80.0,
    "ATTENTION": 60.0,
}


def compute_risk(soil_moisture: float) -> str:
    if soil_moisture >= RISK_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    if soil_moisture >= RISK_THRESHOLDS["ATTENTION"]:
        return "ATTENTION"
    return "SAFE"


async def save_batch(db: AsyncSession, payload: CpdBatchIn) -> dict:
    received = 0
    skipped = 0

    epd_uids = [r.epd_uid for r in payload.readings]
    stmt = select(Epd).where(Epd.epd_uid.in_(epd_uids))
    result = await db.execute(stmt)
    epd_map: dict[str, int] = {epd.epd_uid: epd.id for epd in result.scalars().all()}

    for item in payload.readings:
        epd_id = epd_map.get(item.epd_uid)
        if epd_id is None:
            skipped += 1
            continue

        reading = SensorReading(
            epd_id=epd_id,
            soil_moisture=item.soil_moisture,
            rainfall=item.rainfall,
            temperature=item.temperature,
            lux=item.lux,
            risk_level=compute_risk(item.soil_moisture),
        )
        db.add(reading)
        received += 1

    await db.commit()
    return {"received": received, "skipped": skipped}
