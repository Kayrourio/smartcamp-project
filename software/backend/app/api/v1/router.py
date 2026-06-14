from fastapi import APIRouter
from app.api.v1 import cpd, epd, weather, health

router = APIRouter(prefix="/api/v1")
router.include_router(cpd.router)
router.include_router(epd.router)
router.include_router(weather.router)
router.include_router(health.router)
