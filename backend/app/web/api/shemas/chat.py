"""
Pydantic schemas for chat-related data models.

This module defines Pydantic models used for validating
and serializing chat-related data in the application.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.db.models.chat import ChatType
from app.web.api.shemas.api import ApiResponse


class ChatResponse(BaseModel):
    """
    Chat response schema.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Unique identifier for the chat.")
    title: str = Field(..., description="Title of the chat.")
    username: str = Field(..., description="Unique identifier for the chat.")
    description: Optional[str] = Field(
        None, description="A brief overview of the chat's purpose or content."
    )
    avatar_url: Optional[str] = Field(
        None, description="URL link to the chat's avatar image."
    )
    chat_type: ChatType = Field(..., description="Type of the chat.")
    owner_id: UUID = Field(..., description="User ID of the chat owner.")


class ChatCreateResponse(ApiResponse):
    """
    Response schema for creating a chat.
    """

    chat: Optional[ChatResponse] = Field(None, description="Created chat.")


class ChatCreateRequest(BaseModel):
    """
    Request schema for creating a chat.
    """

    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Title of the chat",
    )
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        description="Username of the chat (if not provided, it will be generated automatically)",
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Description of the chat",
    )
    avatar_url: Optional[str] = Field(
        None,
        description="Avatar URL of the chat",
    )
    chat_type: ChatType = Field(
        default=ChatType.PRIVATE,
        description="Type of the chat",
    )


class ChatUpdateRequest(BaseModel):
    """
    Request schema for updating a chat.
    """

    title: str = Field(
        ..., min_length=1, max_length=100, description="Title of the chat"
    )
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username of the chat"
    )
    chat_type: ChatType = Field(..., description="Type of the chat")
    description: Optional[str] = Field(
        None, max_length=500, description="Description of the chat"
    )
