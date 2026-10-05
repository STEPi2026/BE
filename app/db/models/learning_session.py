from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    duration_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )