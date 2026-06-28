"""
Health response schemas.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health response payload.
    """

    status: str