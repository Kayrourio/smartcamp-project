from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.cpd import CpdBatchIn, CpdBatchOut
from app.services import reading_service

router = APIRouter(prefix="/cpd", tags=["cpd"])


@router.post("/batch", response_model=CpdBatchOut)
async def batch(payload: CpdBatchIn, db: AsyncSession = Depends(get_db)):
    result = await reading_service.save_batch(db, payload)
    return CpdBatchOut(
        received=result["received"],
        skipped=result["skipped"],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
