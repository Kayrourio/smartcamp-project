from datetime import datetime, timezone
from sqlalchemy import String, Numeric, Integer, ForeignKey, DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    epd_id: Mapped[int] = mapped_column(Integer, ForeignKey("epds.id"), nullable=False)
    soil_moisture: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    rainfall: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    temperature: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    lux: Mapped[int | None] = mapped_column(Integer, nullable=True)
    risk_level: Mapped[str] = mapped_column(String(12), nullable=False)
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    epd: Mapped["Epd"] = relationship("Epd", back_populates="readings")

    __table_args__ = (
        Index("idx_readings_epd_received", "epd_id", "received_at"),
        {"sqlite_autoincrement": True},
    )
