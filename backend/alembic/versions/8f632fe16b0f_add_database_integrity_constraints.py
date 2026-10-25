"""add database integrity constraints

Revision ID: 8f632fe16b0f
Revises: 229547335606
Create Date: 2026-10-25 08:13:28.126798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision: str = "8f632fe16b0f"
down_revision: Union[str, Sequence[str], None] = "229547335606"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add database integrity constraints."""

    # Experiences
    op.create_check_constraint(
        "ck_experiences_date_range",
        "experiences",
        "end_date IS NULL OR start_date <= end_date",
    )

    op.create_check_constraint(
        "ck_experiences_current_end_date",
        "experiences",
        "NOT is_current OR end_date IS NULL",
    )

    op.create_check_constraint(
        "ck_experiences_display_order_nonnegative",
        "experiences",
        "display_order >= 0",
    )

    # Projects
    op.create_check_constraint(
        "ck_projects_date_range",
        "projects",
        (
            "start_date IS NULL "
            "OR end_date IS NULL "
            "OR start_date <= end_date"
        ),
    )

    op.create_check_constraint(
        "ck_projects_display_order_nonnegative",
        "projects",
        "display_order >= 0",
    )

    # Skills
    op.create_check_constraint(
        "ck_skills_proficiency_range",
        "skills",
        "proficiency >= 0 AND proficiency <= 100",
    )

    op.create_check_constraint(
        "ck_skills_display_order_nonnegative",
        "skills",
        "display_order >= 0",
    )


def downgrade() -> None:
    """Remove database integrity constraints."""

    op.drop_constraint(
        "ck_skills_display_order_nonnegative",
        "skills",
        type_="check",
    )

    op.drop_constraint(
        "ck_skills_proficiency_range",
        "skills",
        type_="check",
    )

    op.drop_constraint(
        "ck_projects_display_order_nonnegative",
        "projects",
        type_="check",
    )

    op.drop_constraint(
        "ck_projects_date_range",
        "projects",
        type_="check",
    )

    op.drop_constraint(
        "ck_experiences_display_order_nonnegative",
        "experiences",
        type_="check",
    )

    op.drop_constraint(
        "ck_experiences_current_end_date",
        "experiences",
        type_="check",
    )

    op.drop_constraint(
        "ck_experiences_date_range",
        "experiences",
        type_="check",
    )