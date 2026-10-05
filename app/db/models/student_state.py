from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, DECIMAL, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class StudentState(Base):
    __tablename__ = "student_states"

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "concept_id",
            name="uq_student_state_student_concept"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    mastery_score: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 4),
        nullable=False
    )

    knowledge_state: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    weakness_score: Mapped[Decimal] = mapped_column(
        DECIMAL(5, 4),
        nullable=False
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

    concept_id: Mapped[int] = mapped_column(
        ForeignKey("concepts.id"),
        nullable=False
    )