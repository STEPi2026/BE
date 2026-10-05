from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class SkillPrerequisite(Base):
    __tablename__ = "skill_prerequisites"

    skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )

    prerequisite_skill_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("skills.id"),
        primary_key=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )