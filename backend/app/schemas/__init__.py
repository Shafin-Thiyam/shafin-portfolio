"""
Application API schemas.
"""

from app.schemas.common import (
    ApiResponse,
    BaseSchema
)

from app.schemas.health import HealthResponse
from app.schemas.profile import (
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.schemas.skill import (
    SkillCreate,
    SkillListResponse,
    SkillResponse,
    SkillUpdate,
)

from app.schemas.education import (
    EducationCreate,
    EducationResponse,
    EducationUpdate,
    EducationListResponse,
)

from app.schemas.experience import (
    ExperienceCreate,
    ExperienceListResponse,
    ExperienceResponse,
    ExperienceSkillsUpdate,
    ExperienceUpdate
)

__all__ = (
    "ApiResponse",
    "BaseSchema",
    "HealthResponse",
    
    "ProfileCreate",
    "ProfileResponse",
    "ProfileUpdate",
    
    "SkillCreate",
    "SkillUpdate",
    "SkillResponse",
    "SkillListResponse",
    
    "EducationCreate",
    "EducationResponse",
    "EducationUpdate",
    "EducationListResponse",  
    
    "ExperienceCreate",
    "ExperienceListResponse",
    "ExperienceResponse",
    "ExperienceSkillsUpdate",
    "ExperienceUpdate",
)