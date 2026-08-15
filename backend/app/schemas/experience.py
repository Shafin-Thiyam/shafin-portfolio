"""
Experience schemas.
"""

from datetime import date
from datetime import datetime
from typing import Annotated

from pydantic import Field

from app.schemas.common import (
    ApiResponse,
    BaseSchema,
)


class ExperienceCreate(BaseSchema):
    """
    Schema for creating an experience.
    """

    company: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    designation: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    employment_type: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
        ),
    ]

    location: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    location_type: Annotated[
        str,
        Field(
            min_length=1,
            max_length=30,
        ),
    ]

    start_date: date

    end_date: date | None = None

    is_current: bool = False

    description: str | None = None

    display_order: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class ExperienceUpdate(BaseSchema):
    """
    Schema for updating an experience.
    """

    company: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    designation: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    employment_type: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
        ),
    ]

    location: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    location_type: Annotated[
        str,
        Field(
            min_length=1,
            max_length=30,
        ),
    ]

    start_date: date

    end_date: date | None = None

    is_current: bool = False

    description: str | None = None

    display_order: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class ExperienceResponse(BaseSchema):
    """
    Experience response schema.
    """

    id: int
    company: str
    designation: str
    employment_type: str
    location: str
    location_type: str
    start_date: date
    end_date: date | None
    is_current: bool
    description: str | None
    display_order: int
    created_at: datetime
    updated_at: datetime


ExperienceListResponse = ApiResponse[list[ExperienceResponse]]