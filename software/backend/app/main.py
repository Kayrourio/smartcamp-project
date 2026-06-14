from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1.router import router

import app.models.cpd      # noqa: F401
import app.models.epd      # noqa: F401
import app.models.epd_cpd  # noqa: F401
import app.models.reading  # noqa: F401

_NEW_COLUMNS = [
    "ALTER TABLE sensor_readings ADD COLUMN angle_x REAL",
    "ALTER TABLE sensor_readings ADD COLUMN angle_y REAL",
    "ALTER TABLE sensor_readings ADD COLUMN angle_z REAL",
    "ALTER TABLE sensor_readings ADD COLUMN tilt_detected INTEGER NOT NULL DEFAULT 0",
    "ALTER TABLE epds ADD COLUMN is_mock INTEGER NOT NULL DEFAULT 0",
]


async def _migrate(conn):
    for sql in _NEW_COLUMNS:
        try:
            await conn.execute(text(sql))
        except Exception:
            pass  # column already exists


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _migrate(conn)
    yield


app = FastAPI(title="TerraSafe API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
