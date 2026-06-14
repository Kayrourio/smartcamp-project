"""Popula o banco com leituras fake para desenvolvimento."""
import asyncio
import random
from datetime import datetime, timedelta, timezone

from sqlalchemy import text
from app.core.database import engine, Base
from app.models.reading import SensorReading
from app.services.sensor_service import compute_risk
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        now = datetime.now(timezone.utc)
        readings = []
        moisture = 40.0
        for i in range(60):
            ts = now - timedelta(minutes=60 - i)
            moisture = max(0.0, min(100.0, moisture + random.uniform(-3, 5)))
            readings.append(SensorReading(
                sensor_id="EPD-01",
                soil_moisture=round(moisture, 2),
                rainfall=round(random.uniform(0, 25), 2),
                temperature=round(random.uniform(20, 28), 2),
                lux=random.randint(1000, 8000),
                risk_level=compute_risk(moisture),
                created_at=ts,
            ))
        session.add_all(readings)
        await session.commit()
        print(f"Seed: {len(readings)} leituras inseridas. Última umidade: {moisture:.1f}%")


if __name__ == "__main__":
    asyncio.run(seed())
