from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    solution_image_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    solve_time_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    hint_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    attempted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    retry_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    session_id: Mapped[int] = mapped_column(
        ForeignKey("learning_sessions.id"),
        nullable=False
    )

    problem_id: Mapped[int | None] = mapped_column(
        ForeignKey("problems.id"),
        nullable=True
    )

    captured_problem_id: Mapped[int | None] = mapped_column(
        ForeignKey("captured_problems.id"),
        nullable=True
    )

    parent_attempt_id: Mapped[int | None] = mapped_column(
        ForeignKey("attempts.id"),
        nullable=True
    )