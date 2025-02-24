"""
User schemas.
"""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    """
    Database user schema.
    """

    model_config = ConfigDict(extra="allow", from_attributes=True)

    id: UUID = Field(..., description="Unique identifier for the user.")
    telegram_id: int = Field(..., description="Telegram ID of the user.")
    first_name: str | None = Field(None, description="First name of the user.")
    last_name: str | None = Field(None, description="Last name of the user.")
    username: str | None = Field(None, description="Username of the user.")
    photo_url: str | None = Field(None, description="URL of the user's photo.")
