"""
SQLAlchemy declarative base.

All ORM models in the application inherit from this base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.
    """
    pass