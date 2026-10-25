

from datetime import date, datetime
from typing import Annotated

from pydantic import Field, model_validator

from app.schemas.common import BaseSchema


class ProjectCreate(BaseSchema):
    """
    Schema for creating a project.
    """

    @model_validator(mode="after")
    def validate_project_dates(self):
        """Validate project date consistency."""

        if (
            self.start_date is not None
            and self.end_date is not None
            and self.start_date > self.end_date
        ):
            raise ValueError(
                "start_date must be on or before end_date."
            )

        return self

    experience_id: Annotated[
        int,
        Field(gt=0),
    ]

    title: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    description: str | None = None

    role: Annotated[
        str | None,
        Field(max_length=100),
    ] = None

    technologies: list[str] = Field(
        default_factory=list,
        description="Technologies used in the project.",
    )

    project_url: Annotated[
        str | None,
        Field(max_length=500),
    ] = None

    repository_url: Annotated[
        str | None,
        Field(max_length=500),
    ] = None

    start_date: date | None = None

    end_date: date | None = None

    display_order: Annotated[
        int,
        Field(ge=0),
    ]


class ProjectUpdate(BaseSchema):
    """
    Schema for updating a project.

    All editable fields are required in the request.
    Nullable fields may explicitly be set to null.
    """

    @model_validator(mode="after")
    def validate_project_dates(self):
        """Validate project date consistency."""

        if (
            self.start_date is not None
            and self.end_date is not None
            and self.start_date > self.end_date
        ):
            raise ValueError(
                "start_date must be on or before end_date."
            )

        return self

    experience_id: Annotated[
        int,
        Field(gt=0),
    ]

    title: Annotated[
        str,
        Field(
            min_length=1,
            max_length=150,
        ),
    ]

    description: str | None = Field(...)

    role: Annotated[
        str | None,
        Field(max_length=100),
    ] = Field(...)

    technologies: list[str] = Field(
        ...,
        description="Technologies used in the project.",
    )

    project_url: Annotated[
        str | None,
        Field(max_length=500),
    ] = Field(...)

    repository_url: Annotated[
        str | None,
        Field(max_length=500),
    ] = Field(...)

    start_date: date | None = Field(...)

    end_date: date | None = Field(...)

    display_order: Annotated[
        int,
        Field(ge=0),
    ]


class ProjectResponse(BaseSchema):
    """
    Project response schema.
    """

    id: int
    experience_id: int
    title: str
    description: str | None
    role: str | None
    technologies: list[str]
    project_url: str | None
    repository_url: str | None
    start_date: date | None
    end_date: date | None
    display_order: int
    created_at: datetime
    updated_at: datetime
