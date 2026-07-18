"""
Skill schemas.
"""

from datetime import datetime
from typing import Annotated

from pydantic import Field

from app.schemas.common import (
    ApiResponse,
    BaseSchema,
)


class SkillCreate(BaseSchema):
    """
    Schema for creating a skill.
    """

    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
        ),
    ]

    category: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
        ),
    ]

    proficiency: Annotated[
        int,
        Field(
            ge=0,
            le=100,
        ),
    ]

    display_order: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class SkillUpdate(BaseSchema):
    """
    Schema for updating a skill.
    """

    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
        ),
    ]

    category: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
        ),
    ]

    proficiency: Annotated[
        int,
        Field(
            ge=0,
            le=100,
        ),
    ]

    display_order: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class SkillResponse(BaseSchema):
    """
    Skill response schema.
    """

    id: int
    name: str
    category: str
    proficiency: int
    display_order: int
    created_at: datetime
    updated_at: datetime


SkillListResponse = ApiResponse[list[SkillResponse]]