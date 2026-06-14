"""
Populates the database with 1 CPD, 3 EPDs, and fake readings for the last 30 minutes.
Run from backend/: python scripts/seed.py
"""
import asyncio
import random
from datetime import datetime, timedelta, timezone

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.database import Base
from app.models.cpd import Cpd
from app.models.epd import Epd
from app.models.epd_cpd import EpdCpd
from app.models.reading import SensorReading
from app.services.reading_service import compute_risk

import app.models.cpd      # noqa: F401
import app.models.epd      # noqa: F401
import app.models.epd_cpd  # noqa: F401
import app.models.reading  # noqa: F401

EPD_CONFIGS = [
    {"epd_uid": "EPD-001", "label": "TecnoParq", "lat": -20.7136726, "lng": -42.8646703},
]

CPD_CONFIG = {
    "cpd_uid": "CPD-CAMPUS-01",
    "label": "Campus UFV",
    "lat": -20.7546,
    "lng": -42.8825,
}


async def seed():
    engine = create_async_engine(settings.database_url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as db:
        cpd = Cpd(**CPD_CONFIG)
        db.add(cpd)
        await db.flush()

        epds = []
        for cfg in EPD_CONFIGS:
            epd = Epd(**cfg)
            db.add(epd)
            await db.flush()
            epds.append(epd)

            link = EpdCpd(epd_id=epd.id, cpd_id=cpd.id)
            db.add(link)

        now = datetime.now(timezone.utc)
        for epd in epds:
            for minutes_ago in range(30, -1, -2):
                ts = now - timedelta(minutes=minutes_ago)
                moisture = round(random.uniform(40.0, 92.0), 2)
                reading = SensorReading(
                    epd_id=epd.id,
                    soil_moisture=moisture,
                    rainfall=round(random.uniform(0.0, 25.0), 2),
                    temperature=round(random.uniform(20.0, 28.0), 2),
                    lux=random.randint(1000, 9000),
                    risk_level=compute_risk(moisture),
                    received_at=ts,
                )
                db.add(reading)
                await db.flush()  # individual flush avoids bulk-insert RETURNING issues on SQLite

        await db.commit()

    await engine.dispose()
    print("Seed complete: 1 CPD, 3 EPDs, readings for last 30 min.")


if __name__ == "__main__":
    asyncio.run(seed())
