"""
Pydantic schemas for chat messages.

This module defines Pydantic models used for validating
and serializing chat messages in the application.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.web.shemas.paginate import PaginatedResponse
from app.web.shemas.user import UserSchema


class ChatMessageResponse(BaseModel):
    """
    Chat message response schema.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Unique identifier for the message.")
    chat_id: UUID = Field(..., description="ID of the chat the message belongs to.")
    user_id: Optional[UUID] = Field(
        None, description="ID of the user who sent the message."
    )
    user: Optional[UserSchema] = Field(None, description="User who sent the message.")
    content: str = Field(..., description="Content of the message.")
    created_at: str = Field(..., description="Timestamp when the message was created.")


class PaginatedChatMessagesResponse(PaginatedResponse[ChatMessageResponse]):
    """
    Paginated response for chat messages.
    """

    pass
