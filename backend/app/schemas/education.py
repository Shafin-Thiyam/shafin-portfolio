"""
Education schemas.
"""

from datetime import date
from datetime import datetime
from typing import Annotated

from pydantic import Field

from app.schemas.common import (
    ApiResponse,
    BaseSchema,
)


class EducationCreate(BaseSchema):
    """
    Schema for creating an education.
    """

    institution: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    degree: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    field_of_study: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    start_date: date

    end_date: date | None = None

    grade: Annotated[
        str | None,
        Field(
            max_length=50,
        ),
    ] = None

    description: str | None = None

    display_order: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class EducationUpdate(BaseSchema):
    """
    Schema for updating an education.
    """

    institution: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    degree: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    field_of_study: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    start_date: date

    end_date: date | None = None

    grade: Annotated[
        str | None,
        Field(
            max_length=50,
        ),
    ] = None

    description: str | None = None

    display_order: Annotated[
        int,
        Field(
            ge=0,
        ),
    ]


class EducationResponse(BaseSchema):
    """
    Education response schema.
    """

    id: int
    institution: str
    degree: str
    field_of_study: str
    start_date: date
    end_date: date | None
    grade: str | None
    description: str | None
    display_order: int
    created_at: datetime
    updated_at: datetime


EducationListResponse = ApiResponse[list[EducationResponse]]