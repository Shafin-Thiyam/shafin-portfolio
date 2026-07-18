"""
Skill database model.
"""

from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.models.base_model import BaseModel


class Skill(BaseModel):
    """
    Portfolio skill model.
    """

    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
    )

    proficiency: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )