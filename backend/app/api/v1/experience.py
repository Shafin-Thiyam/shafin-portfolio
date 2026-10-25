"""
Experience API endpoints.

This module exposes Experience CRUD operations and collection filters.
Experience-Skill relationship endpoints are implemented in a subsequent
T6 step.
"""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    ApiResponse,
    ExperienceCreate,
    ExperienceListResponse,
    ExperienceResponse,
    ExperienceSkillsUpdate,
    ExperienceUpdate,
)
from app.services import ExperienceService

router = APIRouter()


@router.get(
    "",
    response_model=ExperienceListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get experiences with optional filters",
)
def get_experiences(
    company: Annotated[
        str | None,
        Query(description="Filter by company name (case-insensitive partial match).")] = None,
    employment_type: Annotated[str | None, Query(description="Filter by employment_type(Full-time, Contractual, Part-time).")] = None,
    location_type: Annotated[str | None, Query(description="Filter by location_type(On-site, Remote, Hybrid).")] = None,
    db: Session = Depends(get_db),
) -> ExperienceListResponse:
    """
    Retrieve experiences, optionally filtered by company,
    employment type, and location type.

    When multiple filters are supplied, they are combined
    using AND logic. Company matching is case-insensitive
    partial matching; employment type and location type
    use case-insensitive exact matching.
    """

    service = ExperienceService(db)

    experiences = service.get_filtered(
        company=company,
        employment_type=employment_type,
        location_type=location_type,
    )

    return ExperienceListResponse(
        success=True,
        message="Experiences retrieved successfully.",
        data=[
            ExperienceResponse.model_validate(experience)
            for experience in experiences
        ],
    )


@router.get(
    "/current",
    response_model=ExperienceListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get current experiences",
)
def get_current_experiences(
    db: Session = Depends(get_db),
) -> ExperienceListResponse:
    """Retrieve experiences marked as current."""

    service = ExperienceService(db)
    experiences = service.get_current()

    return ExperienceListResponse(
        success=True,
        message="Current experiences retrieved successfully.",
        data=[
            ExperienceResponse.model_validate(experience)
            for experience in experiences
        ],
    )


@router.get(
    "/{experience_id}",
    response_model=ApiResponse[ExperienceResponse],
    status_code=status.HTTP_200_OK,
    summary="Get experience by ID",
)
def get_experience(
    experience_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[ExperienceResponse]:
    """Retrieve a single experience record."""

    service = ExperienceService(db)
    experience = service.get_by_id(experience_id)

    if experience is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Experience not found.",
        )

    return ApiResponse(
        success=True,
        message="Experience retrieved successfully.",
        data=ExperienceResponse.model_validate(experience),
    )



@router.get(
    "/{experience_id}/skills",
    response_model=ApiResponse[list[int]],
    status_code=status.HTTP_200_OK,
    summary="Get skill IDs associated with an experience",
)
def get_experience_skills(
    experience_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[list[int]]:
    """Retrieve skill IDs associated with an experience."""

    service = ExperienceService(db)

    try:
        skill_ids = service.get_skill_ids(experience_id)
    except ValueError as exc:
        if str(exc) == "Experience not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc

        # Do not hide unexpected service errors.
        raise

    return ApiResponse(
        success=True,
        message="Experience skills retrieved successfully.",
        data=skill_ids,
    )


@router.post(
    "/{experience_id}/skills/{skill_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Associate a skill with an experience",
)
def add_experience_skill(
    experience_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """Associate an existing skill with an experience."""

    service = ExperienceService(db)

    try:
        service.add_skill(experience_id, skill_id)
    except ValueError as exc:
        message = str(exc)

        if message == "Experience not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        if message == "Skill not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        if message == (
            "Skill is already associated with this experience."
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Skill associated with experience successfully.",
        data=None,
    )

@router.put(
    "/{experience_id}/skills",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Replace skills associated with an experience",
)
def update_experience_skills(
    experience_id: int,
    payload: ExperienceSkillsUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """Replace all skills associated with an experience."""

    service = ExperienceService(db)

    try:
        service.set_skills(
            experience_id=experience_id,
            skill_ids=payload.skill_ids,
        )
    except ValueError as exc:
        message = str(exc)

        if message in (
            "Experience not found.",
            "Skill not found.",
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Experience skills updated successfully.",
        data=None,
    )

@router.delete(
    "/{experience_id}/skills/{skill_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Remove a skill association from an experience",
)
def remove_experience_skill(
    experience_id: int,
    skill_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """Remove an associated skill from an experience."""

    service = ExperienceService(db)

    try:
        service.remove_skill(experience_id, skill_id)
    except ValueError as exc:
        message = str(exc)

        if message in (
            "Experience not found.",
            "Skill not found.",
            "Skill is not associated with this experience.",
        ):
            http_status = (
                status.HTTP_409_CONFLICT
                if message == (
                    "Skill is not associated with this experience."
                )
                else status.HTTP_404_NOT_FOUND
            )

            raise HTTPException(
                status_code=http_status,
                detail=message,
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Skill removed from experience successfully.",
        data=None,
    )


@router.post(
    "",
    response_model=ApiResponse[ExperienceResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create experience",
)
def create_experience(
    experience: ExperienceCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[ExperienceResponse]:
    """Create a new portfolio experience record."""

    service = ExperienceService(db)

    try:
        created_experience = service.create(experience)
    except ValueError as exc:
        # ExperienceService raises ValueError for duplicate records.
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return ApiResponse(
        success=True,
        message="Experience created successfully.",
        data=ExperienceResponse.model_validate(created_experience),
    )


@router.put(
    "/{experience_id}",
    response_model=ApiResponse[ExperienceResponse],
    status_code=status.HTTP_200_OK,
    summary="Update experience",
)
def update_experience(
    experience_id: int,
    experience: ExperienceUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[ExperienceResponse]:
    """Update an existing portfolio experience record."""

    service = ExperienceService(db)

    try:
        updated_experience = service.update(
            experience_id,
            experience,
        )
    except ValueError as exc:
        message = str(exc)

        if message == "Experience not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        if message == (
            "An experience with the same company, designation, "
            "and start date already exists."
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            ) from exc

        # Do not hide an unexpected ValueError as a client error.
        raise

    return ApiResponse(
        success=True,
        message="Experience updated successfully.",
        data=ExperienceResponse.model_validate(updated_experience),
    )


@router.delete(
    "/{experience_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete experience",
)
def delete_experience(
    experience_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """Delete an existing portfolio experience record."""

    service = ExperienceService(db)

    try:
        service.delete(experience_id)
    except ValueError as exc:
        if str(exc) == "Experience not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
        raise

    return ApiResponse(
        success=True,
        message="Experience deleted successfully.",
        data=None,
    )
