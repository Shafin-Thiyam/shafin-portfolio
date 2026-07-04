"""
Profile service.
"""

from app.models import Profile
from sqlalchemy.orm import Session

from app.repositories import ProfileRepository


class ProfileService:
    """
    Service layer for profile operations.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        """
        Initialize profile service.

        Args:
            db:
                Active SQLAlchemy session.
        """

        self.repository = ProfileRepository(db)
        
    
    def get_profile(self) -> Profile | None:
        """
        Retrieve the portfolio profile.

        Returns:
            Profile if present, otherwise None.
        """

        return self.repository.get_profile()
    
    def get_profile_by_id(
        self,
        profile_id: int,
    ) -> Profile | None:
        """
        Retrieve a profile by ID.

        Args:
            profile_id:
                Profile identifier.

        Returns:
            Matching profile or None.
        """

        return self.repository.get_by_id(profile_id)

    def get_profile_by_email(
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

        return self.repository.get_by_email(email)
    
    def create_profile(
        self,
        profile: Profile,
    ) -> Profile:
        
        """
        Create a portfolio profile.

        Args:
            profile:
                Profile instance.

        Returns:
            Persisted profile.
        """

        return self.repository.create(profile)
    
    def update_profile(
        self,
        profile: Profile,
    ) -> Profile:
    
        """
        Update the portfolio profile.

        Args:
            profile:
                Updated profile instance.

        Returns:
            Updated profile.
        """

        return self.repository.update(profile)
    
    def delete_profile(
        self,
        profile: Profile,
    ) -> None:
        
        """
        Delete the portfolio profile.

        Args:
            profile:
                Profile to remove.
        """

        self.repository.delete(profile)