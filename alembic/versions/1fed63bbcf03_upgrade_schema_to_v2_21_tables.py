"""upgrade schema to v2 21 tables

Revision ID: 1fed63bbcf03
Revises: d4fa61bb7cde
Create Date: 2026-10-05 19:04:35.000933
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = "1fed63bbcf03"
down_revision: Union[str, Sequence[str], None] = "d4fa61bb7cde"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # ---------------------------------------------------------
    # 1. badges
    # ---------------------------------------------------------
    op.create_table(
        "badges",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("condition_type", sa.String(length=50), nullable=False),
        sa.Column("threshold", sa.Integer(), nullable=False),
        sa.Column("reward_xp", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_badges_code"),
    )

    # ---------------------------------------------------------
    # 2. captured_problems
    # ---------------------------------------------------------
    op.create_table(
        "captured_problems",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("problem_image_url", sa.String(length=500), nullable=False),
        sa.Column("extracted_problem_text", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
            name="fk_captured_problems_student_id",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ---------------------------------------------------------
    # 3. skills
    # ---------------------------------------------------------
    op.create_table(
        "skills",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.String(length=30), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("concept_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["concept_id"],
            ["concepts.id"],
            name="fk_skills_concept_id",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code", name="uq_skills_code"),
    )

    # ---------------------------------------------------------
    # 4. student_badges
    # ---------------------------------------------------------
    op.create_table(
        "student_badges",
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("badge_id", sa.Integer(), nullable=False),
        sa.Column(
            "earned_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["badge_id"],
            ["badges.id"],
            name="fk_student_badges_badge_id",
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
            name="fk_student_badges_student_id",
        ),
        sa.PrimaryKeyConstraint("student_id", "badge_id"),
    )

    # ---------------------------------------------------------
    # 5. student_gamification
    # ---------------------------------------------------------
    op.create_table(
        "student_gamification",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("xp", sa.Integer(), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column("current_streak", sa.Integer(), nullable=False),
        sa.Column("longest_streak", sa.Integer(), nullable=False),
        sa.Column("last_study_date", sa.Date(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
            name="fk_student_gamification_student_id",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_id",
            name="uq_student_gamification_student",
        ),
    )

    # ---------------------------------------------------------
    # 6. problem_skills
    # ---------------------------------------------------------
    op.create_table(
        "problem_skills",
        sa.Column("problem_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["problem_id"],
            ["problems.id"],
            name="fk_problem_skills_problem_id",
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
            name="fk_problem_skills_skill_id",
        ),
        sa.PrimaryKeyConstraint("problem_id", "skill_id"),
    )

    # ---------------------------------------------------------
    # 7. skill_prerequisites
    # ---------------------------------------------------------
    op.create_table(
        "skill_prerequisites",
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("prerequisite_skill_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["prerequisite_skill_id"],
            ["skills.id"],
            name="fk_skill_prerequisites_prerequisite_skill_id",
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
            name="fk_skill_prerequisites_skill_id",
        ),
        sa.PrimaryKeyConstraint(
            "skill_id",
            "prerequisite_skill_id",
        ),
    )

    # ---------------------------------------------------------
    # 8. student_skill_states
    # ---------------------------------------------------------
    op.create_table(
        "student_skill_states",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "mastery_score",
            sa.Numeric(precision=5, scale=4),
            nullable=False,
        ),
        sa.Column(
            "weakness_score",
            sa.Numeric(precision=5, scale=4),
            nullable=False,
        ),
        sa.Column(
            "consecutive_wrong_count",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column("last_practiced_at", sa.DateTime(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
            name="fk_student_skill_states_skill_id",
        ),
        sa.ForeignKeyConstraint(
            ["student_id"],
            ["users.id"],
            name="fk_student_skill_states_student_id",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "student_id",
            "skill_id",
            name="uq_student_skill_states_student_skill",
        ),
    )

    # ---------------------------------------------------------
    # Existing table: attempts
    # ---------------------------------------------------------
    op.add_column(
        "attempts",
        sa.Column("retry_count", sa.Integer(), nullable=False),
    )

    op.add_column(
        "attempts",
        sa.Column("captured_problem_id", sa.Integer(), nullable=True),
    )

    op.add_column(
        "attempts",
        sa.Column("parent_attempt_id", sa.Integer(), nullable=True),
    )

    op.alter_column(
        "attempts",
        "problem_id",
        existing_type=mysql.INTEGER(),
        nullable=True,
    )

    op.create_foreign_key(
        "fk_attempts_captured_problem_id",
        "attempts",
        "captured_problems",
        ["captured_problem_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_attempts_parent_attempt_id",
        "attempts",
        "attempts",
        ["parent_attempt_id"],
        ["id"],
    )

    # ---------------------------------------------------------
    # Existing table: concepts
    # ---------------------------------------------------------
    op.add_column(
        "concepts",
        sa.Column("code", sa.String(length=30), nullable=False),
    )

    op.create_unique_constraint(
        "uq_concepts_code",
        "concepts",
        ["code"],
    )

    # ---------------------------------------------------------
    # Existing table: misconceptions
    # ---------------------------------------------------------
    op.create_unique_constraint(
        "uq_misconceptions_code",
        "misconceptions",
        ["code"],
    )

    # ---------------------------------------------------------
    # Existing table: problems
    # ---------------------------------------------------------
    op.add_column(
        "problems",
        sa.Column("problem_code", sa.String(length=30), nullable=False),
    )

    op.add_column(
        "problems",
        sa.Column("usage", sa.String(length=30), nullable=False),
    )

    op.add_column(
        "problems",
        sa.Column("explanation", sa.Text(), nullable=True),
    )

    op.create_unique_constraint(
        "uq_problems_problem_code",
        "problems",
        ["problem_code"],
    )


def downgrade() -> None:

    # ---------------------------------------------------------
    # Existing table: problems
    # ---------------------------------------------------------
    op.drop_constraint(
        "uq_problems_problem_code",
        "problems",
        type_="unique",
    )

    op.drop_column("problems", "explanation")
    op.drop_column("problems", "usage")
    op.drop_column("problems", "problem_code")

    # ---------------------------------------------------------
    # Existing table: misconceptions
    # ---------------------------------------------------------
    op.drop_constraint(
        "uq_misconceptions_code",
        "misconceptions",
        type_="unique",
    )

    # ---------------------------------------------------------
    # Existing table: concepts
    # ---------------------------------------------------------
    op.drop_constraint(
        "uq_concepts_code",
        "concepts",
        type_="unique",
    )

    op.drop_column("concepts", "code")

    # ---------------------------------------------------------
    # Existing table: attempts
    # ---------------------------------------------------------
    op.drop_constraint(
        "fk_attempts_parent_attempt_id",
        "attempts",
        type_="foreignkey",
    )

    op.drop_constraint(
        "fk_attempts_captured_problem_id",
        "attempts",
        type_="foreignkey",
    )

    op.alter_column(
        "attempts",
        "problem_id",
        existing_type=mysql.INTEGER(),
        nullable=False,
    )

    op.drop_column("attempts", "parent_attempt_id")
    op.drop_column("attempts", "captured_problem_id")
    op.drop_column("attempts", "retry_count")

    # ---------------------------------------------------------
    # New tables - reverse dependency order
    # ---------------------------------------------------------
    op.drop_table("student_skill_states")
    op.drop_table("skill_prerequisites")
    op.drop_table("problem_skills")
    op.drop_table("student_gamification")
    op.drop_table("student_badges")
    op.drop_table("skills")
    op.drop_table("captured_problems")
    op.drop_table("badges")