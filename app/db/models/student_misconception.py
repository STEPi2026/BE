from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, DECIMAL, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class StudentMisconception(Base):
    __tablename__ = "student_misconceptions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    confidence: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 4),
        nullable=False
    )

    detected_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    misconception_id: Mapped[int] = mapped_column(
        ForeignKey("misconceptions.id"),
        nullable=False
    )