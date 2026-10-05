from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class TutorAction(Base):
    __tablename__ = "tutor_actions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    action_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    next_difficulty: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    raw_result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("attempts.id"),
        nullable=False
    )

    ai_analysis_id: Mapped[int] = mapped_column(
        ForeignKey("ai_analysis_results.id"),
        nullable=False
    )

    next_problem_id: Mapped[int | None] = mapped_column(
        ForeignKey("problems.id"),
        nullable=True
    )