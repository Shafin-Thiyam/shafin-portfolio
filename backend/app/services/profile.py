"""
Profile service.
"""

from app.models import Profile
from app.schemas import (
    ProfileCreate,
    ProfileUpdate,
)
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
        profile: ProfileCreate,
    ) -> Profile:
        
        """
        Create a portfolio profile.

        Args:
            profile:
                Profile creation data.

        Returns:
            Persisted profile.
        """
        
        new_profile = Profile(
            full_name=profile.full_name,
            title=profile.title,
            email=profile.email,
            phone=profile.phone,
            location=profile.location,
            linkedin_url=profile.linkedin_url,
            github_url=profile.github_url,
            portfolio_url=profile.portfolio_url,
            summary=profile.summary,
            profile_image=profile.profile_image,
            resume_url=profile.resume_url,
        )

        return self.repository.create(new_profile)
    
    def update_profile(
        self,
        profile: ProfileUpdate,
    ) -> Profile:
    
        """
        Update the portfolio profile.

        Args:
            profile:
                Updated profile data.

        Returns:
            Updated profile.
        """
        existing_profile = self.repository.get_profile()
        
        if existing_profile is None:
            raise ValueError("Profile not found.")
        
        existing_profile.full_name = profile.full_name
        existing_profile.title = profile.title
        existing_profile.email = profile.email
        existing_profile.phone = profile.phone
        existing_profile.location = profile.location
        existing_profile.linkedin_url = profile.linkedin_url
        existing_profile.github_url = profile.github_url
        existing_profile.portfolio_url = profile.portfolio_url
        existing_profile.summary = profile.summary
        existing_profile.profile_image = profile.profile_image
        existing_profile.resume_url = profile.resume_url

        return self.repository.update(existing_profile)
    
    def delete_profile(self) -> None:
        """
        Delete the portfolio profile.
        """

        existing_profile = self.repository.get_profile()

        if existing_profile is None:
            raise ValueError("Profile not found.")

        self.repository.delete(existing_profile)
    