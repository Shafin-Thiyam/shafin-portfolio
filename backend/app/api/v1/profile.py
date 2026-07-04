"""
Profile API endpoints.
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status)

from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    ApiResponse,
    ProfileCreate,
    ProfileResponse,
    ProfileUpdate,
)
from app.services import ProfileService

router = APIRouter()

@router.get(
    "",
    response_model=ApiResponse[ProfileResponse],
    summary="Get portfolio profile",
)
def get_profile(
    db: Session = Depends(get_db),
) -> ApiResponse[ProfileResponse]:
    """
    Retrieve the portfolio profile.
    """

    service = ProfileService(db)

    profile = service.get_profile()
    
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )


    return ApiResponse(
        success=True,
        message="Profile retrieved successfully.",
        data=ProfileResponse.model_validate(profile),
    )

@router.post(
    "",
    response_model=ApiResponse[ProfileResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create portfolio profile",
)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
) -> ApiResponse[ProfileResponse]:
    """
    Create the portfolio profile.
    """

    service = ProfileService(db)

    created_profile = service.create_profile(profile)

    return ApiResponse(
        success=True,
        message="Profile created successfully.",
        data=ProfileResponse.model_validate(created_profile),
    )


@router.put(
    "",
    response_model=ApiResponse[ProfileResponse],
    status_code=status.HTTP_200_OK,
    summary="Update portfolio profile",
)
def update_profile(
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
) -> ApiResponse[ProfileResponse]:
    """
    Update the portfolio profile.
    """

    service = ProfileService(db)
    
    try:
        updated_profile = service.update_profile(profile)
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )

    return ApiResponse(
        success=True,
        message="Profile updated successfully.",
        data=ProfileResponse.model_validate(updated_profile),
    )
    

@router.delete(
    "",
    response_model=ApiResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete portfolio profile",
)
def delete_profile(
    db: Session = Depends(get_db),
) -> ApiResponse[None]:
    """
    Delete the portfolio profile.
    """

    service = ProfileService(db)

    try:
        service.delete_profile()

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found.",
        )


    return ApiResponse(
        success=True,
        message="Profile deleted successfully.",
        data=None,
    )