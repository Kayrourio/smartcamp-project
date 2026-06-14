import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.main import app as fastapi_app
from app.core.database import Base, get_db
from app.models.epd import Epd

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
async def test_batch_with_known_epd(client, db_session):
    epd = Epd(epd_uid="EPD-TEST-01", label="Test EPD", lat=-20.75, lng=-42.88)
    db_session.add(epd)
    await db_session.flush()
    await db_session.commit()

    payload = {
        "cpd_uid": "CPD-TEST-01",
        "readings": [
            {"epd_uid": "EPD-TEST-01", "soil_moisture": 85.0, "rainfall": 10.0, "temperature": 24.0, "lux": 3000}
        ],
    }
    resp = await client.post("/api/v1/cpd/batch", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["received"] == 1
    assert data["skipped"] == 0


@pytest.mark.asyncio
async def test_batch_with_unknown_epd(client, db_session):
    payload = {
        "cpd_uid": "CPD-TEST-01",
        "readings": [
            {"epd_uid": "EPD-UNKNOWN", "soil_moisture": 50.0}
        ],
    }
    resp = await client.post("/api/v1/cpd/batch", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["received"] == 0
    assert data["skipped"] == 1


@pytest.mark.asyncio
async def test_batch_mixed(client, db_session):
    epd = Epd(epd_uid="EPD-REAL-01", label="Real EPD")
    db_session.add(epd)
    await db_session.flush()
    await db_session.commit()

    payload = {
        "cpd_uid": "CPD-TEST-01",
        "readings": [
            {"epd_uid": "EPD-REAL-01", "soil_moisture": 70.0},
            {"epd_uid": "EPD-GHOST",   "soil_moisture": 55.0},
        ],
    }
    resp = await client.post("/api/v1/cpd/batch", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["received"] == 1
    assert data["skipped"] == 1
