from datetime import datetime, timezone
from sqlalchemy import Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EpdCpd(Base):
    __tablename__ = "epd_cpd"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    epd_id: Mapped[int] = mapped_column(Integer, ForeignKey("epds.id", ondelete="CASCADE"), nullable=False)
    cpd_id: Mapped[int] = mapped_column(Integer, ForeignKey("cpds.id", ondelete="CASCADE"), nullable=False)
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    __table_args__ = (UniqueConstraint("epd_id", "cpd_id", name="uq_epd_cpd"),)

    epd: Mapped["Epd"] = relationship("Epd", back_populates="cpd_links")
    cpd: Mapped["Cpd"] = relationship("Cpd", back_populates="epd_links")
