import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app as fastapi_app
from app.core.database import Base, get_db
from app.models.epd import Epd
from app.models.reading import SensorReading

import app.models.cpd
import app.models.epd
import app.models.epd_cpd
import app.models.reading

TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DB_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        yield session
    await engine.dispose()


@pytest_asyncio.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session

    fastapi_app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as ac:
        yield ac

    fastapi_app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_list_epds_empty(client, db_session):
    resp = await client.get("/api/v1/epd/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_list_epds_with_latest(client, db_session):
    epd = Epd(epd_uid="EPD-001", label="Norte", lat=-20.75, lng=-42.88)
    db_session.add(epd)
    await db_session.flush()

    reading = SensorReading(
        epd_id=epd.id,
        soil_moisture=87.2,
        rainfall=18.4,
        temperature=23.8,
        lux=3200,
        risk_level="CRITICAL",
    )
    db_session.add(reading)
    await db_session.flush()
    await db_session.commit()

    resp = await client.get("/api/v1/epd/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["epd_uid"] == "EPD-001"
    assert data[0]["latest"]["risk_level"] == "CRITICAL"
    assert data[0]["latest"]["soil_moisture"] == 87.2


@pytest.mark.asyncio
async def test_epd_history_unknown(client, db_session):
    resp = await client.get("/api/v1/epd/EPD-GHOST/history")
    assert resp.status_code == 200
    data = resp.json()
    assert data["epd_uid"] == "EPD-GHOST"
    assert data["readings"] == []
