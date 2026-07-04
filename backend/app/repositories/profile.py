"""
Profile repository.
"""

from sqlalchemy.orm import Session

from app.models import Profile
from app.repositories import BaseRepository


class ProfileRepository(BaseRepository[Profile]):
    """
    Repository for Profile operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize repository.

        Args:
            db:
                Active SQLAlchemy session.
        """

        super().__init__(
            db=db,
            model=Profile,
        )