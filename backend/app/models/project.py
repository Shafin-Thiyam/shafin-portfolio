"""
Project database model.
"""

from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.base_model import BaseModel


class Project(BaseModel):
    """
    Portfolio project model.
    """

    __tablename__ = "projects"

    experience_id: Mapped[int] = mapped_column(
        ForeignKey(
            "experiences.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    role: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    technologies: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    project_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    repository_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    experience: Mapped["Experience"] = relationship(
        "Experience",
        back_populates="projects",
    )