"""
Application database models.
"""

from app.models.base_model import BaseModel
from app.models.profile import Profile

__all__ = (
    "BaseModel",
    "Profile",
)