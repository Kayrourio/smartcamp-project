from datetime import datetime, timezone
from sqlalchemy import String, Numeric, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Epd(Base):
    __tablename__ = "epds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    epd_uid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lat: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    lng: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_mock: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    cpd_links: Mapped[list["EpdCpd"]] = relationship("EpdCpd", back_populates="epd")
    readings: Mapped[list["SensorReading"]] = relationship("SensorReading", back_populates="epd")
