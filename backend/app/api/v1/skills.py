"""
Skill API endpoints.
"""
from typing import Annotated
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Query,
)
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    ApiResponse,
    SkillListResponse,
    SkillResponse,
    SkillCreate,
    SkillUpdate,
)

from app.services import SkillService

router = APIRouter()


@router.get(
    "",
    response_model=SkillListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all skills",
)
def get_skills(
    category: Annotated[
        str | None,
        Query(
            description="Filter skills by category.",
        ),
    ] = None,
    db: Session = Depends(get_db),
) -> SkillListResponse:
    """
    Retrieve all portfolio skills.
    """

    service = SkillService(db)
    
    if category:
        skills = service.get_skills_by_category(category)
    else:
        skills = service.get_all_skills()
    #skills = service.get_all_skills()

    return SkillListResponse(
        success=True,
        message="Skills retrieved successfully.",
        data=[
            SkillResponse.model_validate(skill)
            for skill in skills
        ],
    )

@router.get(
    "/{skill_id}",
    response_model=ApiResponse[SkillResponse],
    status_code=status.HTTP_200_OK,
    summary="Get skill by ID",
)
def get_skill(
    skill_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[SkillResponse]:
    """
    Retrieve a single skill.
    """

    service = SkillService(db)

    skill = service.get_skill(skill_id)

    if skill is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found.",
        )

    return ApiResponse(
        success=True,
        message="Skill retrieved successfully.",
        data=SkillResponse.model_validate(skill),
    )
    
@router.post(
    "",
    response_model=ApiResponse[SkillResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create skill",
)
def create_skill(
    skill: SkillCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[SkillResponse]:
    """
    Create a new portfolio skill.
    """

    service = SkillService(db)

    try:
        created_skill = service.create_skill(skill)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return ApiResponse(
        success=True,
        message="Skill created successfully.",
        data=SkillResponse.model_validate(created_skill),
    )
    
@router.put(
    "/{skill_id}",
    response_model=ApiResponse[SkillResponse],
    status_code=status.HTTP_200_OK,
    summary="Update skill",
)
def update_skill(
    skill_id: int,
    skill: SkillUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[SkillResponse]:
    """
    Update an existing portfolio skill.
    """

    service = SkillService(db)

    try:
        updated_skill = service.update_skill(
            skill_id,
            skill,
        )

    except ValueError as exc:

        message = str(exc)

        if message == "Skill not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        if message == "Skill already exists.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Skill updated successfully.",
        data=SkillResponse.model_validate(updated_skill),
    )
    
@router.delete(
    "/{skill_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete skill",
)
def delete_skill(
    skill_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """
    Delete a portfolio skill.
    """

    service = SkillService(db)

    try:
        service.delete_skill(skill_id)

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ApiResponse(
        success=True,
        message="Skill deleted successfully.",
        data=None,
    )