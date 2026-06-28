"""
Health check endpoints.
"""

from fastapi import APIRouter


router = APIRouter()


@router.get(
    "",
    summary="Health Check",
    description="Returns the health status of the application.",
)
async def health_check() -> dict[str, str]:
    """
    Check if the application is running.

    Returns:
        dict[str, str]: Application health status.
    """
    return {"status": "healthy"}