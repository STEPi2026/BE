from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, DECIMAL, ForeignKey, Integer, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class AIAnalysisResult(Base):
    __tablename__ = "ai_analysis_results"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    mastery_score: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 4),
        nullable=False
    )

    first_error_step: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    confidence: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 4),
        nullable=False
    )

    raw_result: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    attempt_id: Mapped[int] = mapped_column(
        ForeignKey("attempts.id"),
        nullable=False
    )

    misconception_id: Mapped[int | None] = mapped_column(
        ForeignKey("misconceptions.id"),
        nullable=True
    )