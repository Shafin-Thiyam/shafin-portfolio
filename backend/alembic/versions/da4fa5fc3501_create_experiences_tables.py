"""create experiences tables

Revision ID: da4fa5fc3501
Revises: e2a2390a5e71
Create Date: 2026-08-15 12:55:02.159714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da4fa5fc3501'
down_revision: Union[str, Sequence[str], None] = 'e2a2390a5e71'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "experiences",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "company",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "designation",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "employment_type",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "location",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "location_type",
            sa.String(length=30),
            nullable=False,
        ),
        sa.Column(
            "start_date",
            sa.Date(),
            nullable=False,
        ),
        sa.Column(
            "end_date",
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            "is_current",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
        sa.Column(
            "description",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "display_order",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    
    op.create_index(
        op.f("ix_experiences_display_order"),
        "experiences",
        ["display_order"],
        unique=False,
    )
    
    op.create_table(
        "experience_skills",
        sa.Column(
            "experience_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "skill_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["experience_id"],
            ["experiences.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skills.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint(
            "experience_id",
            "skill_id",
        ),
    )
    
    op.create_index(
        op.f("ix_experience_skills_skill_id"),
        "experience_skills",
        ["skill_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_experience_skills_skill_id"),
        table_name="experience_skills",
    )

    op.drop_table("experience_skills")

    op.drop_index(
        op.f("ix_experiences_display_order"),
        table_name="experiences",
    )

    op.drop_table("experiences")