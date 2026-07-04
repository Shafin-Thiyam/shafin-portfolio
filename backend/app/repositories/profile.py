"""
Profile repository.
"""

from sqlalchemy import select
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

    def get_profile(self) -> Profile | None:
        """
        Retrieve the portfolio profile.

        Returns:
            Profile instance if present, otherwise None.
        """

        statement = select(Profile).limit(1)

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> Profile | None:
        """
        Retrieve a profile by email address.

        Args:
            email:
                Email address.

        Returns:
            Matching profile or None.
        """

        statement = (
            select(Profile)
            .where(Profile.email == email)
        )

        return self.db.scalar(statement)