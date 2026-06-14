from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.epd import EpdOut, EpdHistoryOut
from app.services import epd_service

router = APIRouter(prefix="/epd", tags=["epd"])


@router.get("/", response_model=list[EpdOut])
async def list_epds(db: AsyncSession = Depends(get_db)):
    return await epd_service.get_all_with_latest(db)


@router.get("/{epd_uid}/history", response_model=EpdHistoryOut)
async def history(
    epd_uid: str,
    minutes: int = Query(default=10, ge=1, le=1440),
    db: AsyncSession = Depends(get_db),
):
    return await epd_service.get_history(db, epd_uid, minutes)
