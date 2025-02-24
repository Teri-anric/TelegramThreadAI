from typing import Generic, List, TypeVar, Optional

from pydantic import BaseModel, Field, ConfigDict

T = TypeVar('T')

class PaginationParams(BaseModel):
    """
    Pagination query parameters.
    """
    page: int = Field(1, ge=1, description="Page number")
    per_page: int = Field(50, ge=1, le=100, description="Number of items per page")

class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic paginated response schema.
    """
    model_config = ConfigDict(from_attributes=True)

    items: List[T]

    total_items: int = Field(..., description="Total number of items")
    total_pages: int = Field(..., description="Total number of pages")
    
    has_next: bool = Field(..., description="Has next page")
    has_previous: bool = Field(..., description="Has previous page")
    
    next_page: int | None = Field(None, description="Next page number")
    previous_page: int | None = Field(None, description="Previous page number")
