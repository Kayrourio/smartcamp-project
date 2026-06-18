from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.epd import Epd
from app.models.reading import SensorReading
from app.schemas.cpd import CpdBatchIn

RISK_THRESHOLDS = {
    "CRITICAL": 70.0,
    "HIGH": 25.0,
    "ATTENTION": 10.0,
}
TILT_THRESHOLD = 45.0  # degrees,upright X ≈ -90, fallen X ≈ 0; tilted when abs(x) < threshold


def is_tilted(angle_x: float | None, angle_y: float | None) -> bool:
    # Sensor is upright when X ≈ -90; lying down (fallen) when X ≈ 0
    ax = abs(angle_x) if angle_x is not None else 90.0
    return ax < TILT_THRESHOLD


def compute_risk(soil_moisture: float, angle_x: float | None = None, angle_y: float | None = None) -> str:
    tilted = is_tilted(angle_x, angle_y)

    if tilted:
        # Fallen + wet soil → imminent landslide
        if soil_moisture >= RISK_THRESHOLDS["HIGH"]:
            return "CRITICAL"
        # Fallen + dry soil → alert only
        return "ATTENTION"

    if soil_moisture >= RISK_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    if soil_moisture >= RISK_THRESHOLDS["HIGH"]:
        return "HIGH"
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
            angle_x=item.angle_x,
            angle_y=item.angle_y,
            angle_z=item.angle_z,
            tilt_detected=is_tilted(item.angle_x, item.angle_y),
            risk_level=compute_risk(item.soil_moisture, item.angle_x, item.angle_y),
        )
        db.add(reading)
        received += 1

    await db.commit()
    return {"received": received, "skipped": skipped}
