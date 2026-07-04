"""
Profile API schemas.
"""

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ProfileResponse(BaseModel):
    """
    Profile response schema.
    """

    id: int

    full_name: str

    title: str

    email: str

    phone: str | None

    location: str | None

    linkedin_url: str | None

    github_url: str | None

    portfolio_url: str | None

    summary: str

    profile_image: str | None

    resume_url: str | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
    
class ProfileCreate(BaseModel):
    """
    Profile creation schema.
    """

    full_name: str

    title: str

    email: str

    phone: str | None = None

    location: str | None = None

    linkedin_url: str | None = None

    github_url: str | None = None

    portfolio_url: str | None = None

    summary: str

    profile_image: str | None = None

    resume_url: str | None = None

class ProfileUpdate(BaseModel):
    """
    Profile update schema.
    """

    full_name: str

    title: str

    email: str

    phone: str | None = None

    location: str | None = None

    linkedin_url: str | None = None

    github_url: str | None = None

    portfolio_url: str | None = None

    summary: str

    profile_image: str | None = None

    resume_url: str | None = None