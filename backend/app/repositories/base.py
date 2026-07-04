"""
Generic repository foundation.

All repositories inherit from this class.
"""

from typing import Generic
from typing import Type
from typing import TypeVar

from sqlalchemy.orm import Session

from app.db import Base

ModelType = TypeVar(
    "ModelType",
    bound=Base,
)
class BaseRepository(Generic[ModelType]):
    """
    Base repository for SQLAlchemy models.
    """
    def __init__(
        self,
        db: Session,
        model: Type[ModelType],) -> None:
        """
        Initialize repository.

        Args:
            db:
                Active SQLAlchemy session.

            model:
                SQLAlchemy model handled by this repository.
        """

        self.db = db
        self.model = model