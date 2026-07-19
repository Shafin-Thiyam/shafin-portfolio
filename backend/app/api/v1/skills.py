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