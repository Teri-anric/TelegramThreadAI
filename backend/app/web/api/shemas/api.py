from typing import Literal
from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    status: Literal["ok", "error"] = Field(..., description="Status of the API response.")
    message: str | None = Field(None, description="Optional message providing additional information about the response.")
