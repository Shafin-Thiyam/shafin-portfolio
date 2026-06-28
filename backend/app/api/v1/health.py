"""
Health check endpoints.
"""

from fastapi import APIRouter

from app.schemas.common import ApiResponse
from app.schemas.health import HealthResponse


router = APIRouter()


#@router.get(
#    "",
#    summary="Health Check",
#    description="Returns the health status of the application.",
#)
#async def health_check() -> dict[str, str]:
#    """
#    Check if the application is running.

#    Returns:
#        dict[str, str]: Application health status.
#    """
#    return {"status": "healthy"}



@router.get(
    "",
    response_model=ApiResponse[HealthResponse],
    summary="Health Check",
    description="Returns the health status of the application.",
)
async def health_check() -> ApiResponse[HealthResponse]:
    return ApiResponse(
        success=True,
        message="Application is healthy.",
        data=HealthResponse(
            status="healthy",
        ),
    )