from fastapi import APIRouter
from app.api.v1 import sensors, health

router = APIRouter(prefix="/api/v1")
router.include_router(sensors.router, tags=["sensors"])
router.include_router(health.router, tags=["health"])
