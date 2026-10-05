from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class StudentBadge(Base):
    __tablename__ = "student_badges"

    student_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    badge_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("badges.id"),
        primary_key=True
    )

    earned_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )