from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class StudentGamification(Base):
    __tablename__ = "student_gamification"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            name="uq_student_gamification_student"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    xp: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )

    current_streak: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    longest_streak: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    last_study_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )