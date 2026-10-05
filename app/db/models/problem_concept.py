from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProblemConcept(Base):
    __tablename__ = "problem_concepts"

    problem_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("problems.id"),
        primary_key=True
    )

    concept_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("concepts.id"),
        primary_key=True
    )