from datetime import datetime, timezone
from sqlalchemy import String, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Cpd(Base):
    __tablename__ = "cpds"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cpd_uid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    label: Mapped[str | None] = mapped_column(String(128), nullable=True)
    lat: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    lng: Mapped[float | None] = mapped_column(Numeric(9, 6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    epd_links: Mapped[list["EpdCpd"]] = relationship("EpdCpd", back_populates="cpd")
