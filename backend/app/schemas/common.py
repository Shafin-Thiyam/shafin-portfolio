"""
Common API schemas.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T", bound=BaseModel)




class ApiResponse(BaseModel, Generic[T]):
    """
    Standard API response model.
    """
    
    success: bool = Field(
    description="Indicates whether the request was successful."
)

    message: str = Field(
        description="Human-readable response message."
    )

    data: T = Field(
        description="Response payload."
    )

