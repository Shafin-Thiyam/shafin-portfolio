"""
Common API schemas.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field


T = TypeVar("T", bound=BaseModel)

class BaseSchema(BaseModel):
    """
    Base schema for all request/response models.
    """

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid",
        str_strip_whitespace=True,
    )



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

    data: T | None = Field(
        default=None,
        description="Response payload."
    )

