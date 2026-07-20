"""
Education database model.
"""

from datetime import date

from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import BaseModel


class Education(BaseModel):
    """
    Portfolio education model.
    """

    __tablename__ = "educations"

    institution: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    degree: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    field_of_study: Mapped[str] = mapped_column(
        String(150),
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

    grade: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )