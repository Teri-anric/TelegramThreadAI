"""
Base Pydantic schemas for API responses.

This module defines base Pydantic models used for standardizing
API response structures across the application.
"""

from typing import Literal

from pydantic import BaseModel, Field


class ResponseStatus(BaseModel):
    """
    A standard response status model for API endpoints.

    This model provides a consistent way to return status information
    in API responses, allowing for easy error handling and status tracking.
    """

    status: str = Field(description="The status of the API response.")


class ApiResponse(BaseModel):
    """
    A standard API response model for all endpoints.

    This model provides a consistent way to return status information
    in API responses, allowing for easy error handling and status tracking.
    """

    status: Literal["ok", "error"] = Field(
        ..., description="Status of the API response."
    )
    message: str | None = Field(
        None,
        description="Optional message providing additional information about the response.",
    )
