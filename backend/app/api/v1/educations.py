"""
Education API endpoints.
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
    EducationListResponse,
    EducationResponse,
    EducationCreate,
    EducationUpdate,
)

from app.services import EducationService

router = APIRouter()


@router.get(
    "",
    response_model=EducationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get all educations",
)
def get_educations(
     degree: Annotated[
        str | None,
        Query(),
    ] = None,
    field_of_study: Annotated[
        str | None,
        Query(),
    ] = None,
    db: Session = Depends(get_db),
) -> EducationListResponse:
    
    """
    Retrieve all portfolio education records.
    """

    service = EducationService(db)
    
    if degree is not None:
        educations = service.get_educations_by_degree(degree)
        
    elif field_of_study is not None:
        educations = service.get_educations_by_field_of_study(
            field_of_study
        )
    
    else:
        educations = service.get_all_educations()

    return EducationListResponse(
        success=True,
        message="Educations retrieved successfully.",
        data=[
            EducationResponse.model_validate(education)
            for education in educations
        ],
    )

@router.get(
    "/{education_id}",
    response_model=ApiResponse[EducationResponse],
    status_code=status.HTTP_200_OK,
    summary="Get education by ID",
)
def get_education(
    education_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[EducationResponse]:
    
    """
    Retrieve a single education record.
    """

    service = EducationService(db)

    education = service.get_education(education_id)

    if education is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education not found.",
        )

    return ApiResponse(
        success=True,
        message="Education retrieved successfully.",
        data=EducationResponse.model_validate(education),
    )
    
@router.post(
    "",
    response_model=ApiResponse[EducationResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create Education",
)
def create_education(
    education: EducationCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[EducationResponse]:
    """
    Create a new portfolio education.
    """

    service = EducationService(db)

    try:
        created_education = service.create_education(education)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc

    return ApiResponse(
        success=True,
        message="Education created successfully.",
        data=EducationResponse.model_validate(created_education),
    )
    
@router.put(
    "/{education_id}",
    response_model=ApiResponse[EducationResponse],
    status_code=status.HTTP_200_OK,
    summary="Update Education",
)
def update_education(
    education_id: int,
    education: EducationUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[EducationResponse]:
    """
    Update an existing portfolio education record.
    """

    service = EducationService(db)

    try:
        updated_education = service.update_education(
            education_id,
            education,
        )

    except ValueError as exc:

        message = str(exc)

        if message == "Education not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message,
            ) from exc

        if message == "Education already exists.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=message,
            ) from exc

        raise

    return ApiResponse(
        success=True,
        message="Education updated successfully.",
        data=EducationResponse.model_validate(updated_education),
    )
    
@router.delete(
    "/{education_id}",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete education",
)
def delete_education(
    education_id: int,
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    
    """
    Delete a portfolio education record.
    """

    service = EducationService(db)

    try:
        service.delete_education(education_id)

    except ValueError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    return ApiResponse(
        success=True,
        message="Education deleted successfully.",
        data=None,
    )