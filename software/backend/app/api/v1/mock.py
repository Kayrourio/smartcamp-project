import math
import random
from datetime import datetime, timezone

from fastapi import APIRouter

from app.schemas.epd import EpdOut, ReadingOut

router = APIRouter(prefix="/mock", tags=["mock"])

_CENTER_LAT = -20.7546
_CENTER_LNG = -42.8825


def _make_positions() -> list[tuple[float, float]]:
    """100 deterministic positions spread around Viçosa (seeded)."""
    rng = random.Random(42)
    out = []
    for _ in range(100):
        angle = rng.uniform(0, 2 * math.pi)
        r = rng.uniform(0.003, 0.022)
        lat = _CENTER_LAT + r * math.cos(angle)
        lng = _CENTER_LNG + r * math.sin(angle) * 1.15
        out.append((round(lat, 6), round(lng, 6)))
    return out


_POSITIONS = _make_positions()

# Risk distribution: mostly HIGH/CRITICAL, some ATTENTION/SAFE for realism
_RISK_POOL = ["CRITICAL"] * 25 + ["HIGH"] * 40 + ["ATTENTION"] * 20 + ["SAFE"] * 15


def _make_reading(risk: str) -> ReadingOut:
    rng = random.Random()
    if risk == "CRITICAL":
        moisture = rng.uniform(70, 95)
        tilt = rng.random() < 0.45
    elif risk == "HIGH":
        moisture = rng.uniform(25, 70)
        tilt = rng.random() < 0.08
    else:
        moisture = rng.uniform(10, 25)
        tilt = False

    angle_x = rng.uniform(-30, 20) if tilt else rng.uniform(-95, -78)

    return ReadingOut(
        soil_moisture=round(moisture, 1),
        rainfall=round(rng.uniform(0, 45), 1),
        temperature=round(rng.uniform(18, 34), 1),
        angle_x=round(angle_x, 1),
        angle_y=round(rng.uniform(-5, 5), 1),
        angle_z=round(rng.uniform(-5, 5), 1),
        tilt_detected=tilt,
        risk_level=risk,
        received_at=datetime.now(timezone.utc),
    )


@router.get("/epds", response_model=list[EpdOut])
def get_mock_epds():
    result = []
    for i, (lat, lng) in enumerate(_POSITIONS):
        risk = random.choice(_RISK_POOL)
        result.append(
            EpdOut(
                epd_uid=f"MOCK-{i + 1:03d}",
                label=f"Sensor {i + 1}",
                lat=lat,
                lng=lng,
                active=True,
                latest=_make_reading(risk),
            )
        )
    return result
