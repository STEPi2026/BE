from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class ProblemSkill(Base):
    __tablename__ = "problem_skills"

    problem_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("problems.id"),
        primary_key=True
    )

    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )