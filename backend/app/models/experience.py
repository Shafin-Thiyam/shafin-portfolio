"""
Experience database model.
"""

from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import Index
from app.db import Base
from app.models.base_model import BaseModel


experience_skills = Table(
    "experience_skills",
    Base.metadata,
    Column(
        "experience_id",
        Integer,
        ForeignKey(
            "experiences.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "skill_id",
        Integer,
        ForeignKey(
            "skills.id",
            ondelete="CASCADE",
        ),
        primary_key=True,
        nullable=False,
    ),
    Index(
        "ix_experience_skills_skill_id",
        "skill_id",
    ),
)

class Experience(BaseModel):
    """
    Portfolio experience model.
    """

    __tablename__ = "experiences"

    company: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    designation: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    employment_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    location: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    location_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )