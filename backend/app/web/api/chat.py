"""
Chat API endpoints.

This module provides API routes for managing chat-related operations,
including creating, updating, and retrieving chat information.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.models.chat_member import ChatMemberStatus
from app.db.models.user import User
from app.db.repos.chat import ChatRepository
from app.db.repos.chat_member import ChatMemberRepository
from app.db.repos.exptions import ChatUsernameAlreadyExistsException
from app.web.api.shemas.api import ApiResponse

from ..depends import get_current_user, get_repo
from .shemas.chat import (ChatCreateRequest, ChatCreateResponse, ChatResponse,
                          ChatUpdateRequest)

chat_router = APIRouter(prefix="/chats", tags=["chats"])


@chat_router.post("/", response_model=ChatResponse)
async def create_chat(
    chat_data: ChatCreateRequest,
    user: User = Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_repo(ChatRepository)),
):
    """
    Create a new chat.

    Returns:
        ChatCreateResponse: The response containing the created chat information.
    """
    try:
        # Create chat
        new_chat = await chat_repo.create_chat(
            owner_id=user.id,
            title=chat_data.title,
            username=chat_data.username,
            description=chat_data.description,
            avatar_url=chat_data.avatar_url,
            chat_type=chat_data.chat_type,
        )

        return ChatCreateResponse(
            status="ok", message="Chat created successfully", chat=new_chat
        )
    except ChatUsernameAlreadyExistsException:
        return ApiResponse(status="error", message="Chat username already exists")


@chat_router.get("/{chat_id}", response_model=ChatResponse)
async def get_chat(
    chat_id: UUID, chat_repo: ChatRepository = Depends(get_repo(ChatRepository))
):
    """Retrieve a chat by its ID.

    Args:
        chat_id (UUID): The ID of the chat to retrieve.
        chat_repo (ChatRepository): The repository for chat operations.

    Returns:
        ChatResponse: The response containing the chat information.
    """
    chat = await chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    return ChatResponse.model_validate(chat)


@chat_router.get("/u/{username}", response_model=ChatResponse)
async def get_chat_by_username(
    username: str, chat_repo: ChatRepository = Depends(get_repo(ChatRepository))
):
    """Retrieve a chat by its username.

    Args:
        username (str): The username of the chat to retrieve.
        chat_repo (ChatRepository): The repository for chat operations.

    Returns:
        ChatResponse: The response containing the chat information.
    """
    chat = await chat_repo.get_chat_by_username(username)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )

    return ChatResponse.model_validate(chat)


@chat_router.put("/{chat_id}", response_model=ChatResponse)
async def update_chat(
    chat_id: UUID,
    chat_data: ChatUpdateRequest,
    chat_repo: ChatRepository = Depends(get_repo(ChatRepository)),
    chat_member_repo: ChatMemberRepository = Depends(get_repo(ChatMemberRepository)),
    user: User = Depends(get_current_user),
):
    """Update an existing chat.

    Args:
        chat_id (UUID): The ID of the chat to update.
        chat_data (ChatUpdateRequest): The updated data for the chat.

    Returns:
        ApiResponse: The response indicating the result of the update operation.
    """
    chat_member = await chat_member_repo.get_chat_member(chat_id, user.id)
    if not chat_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of this chat",
        )
    if chat_member.status in [ChatMemberStatus.ADMIN, ChatMemberStatus.OWNER]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You are not an admin of this chat",
        )
    try:
        is_updated = await chat_repo.update_chat(
            chat_id=chat_id,
            title=chat_data.title,
            username=chat_data.username,
            description=chat_data.description,
            chat_type=chat_data.chat_type,
        )
        if not is_updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
            )
    except ChatUsernameAlreadyExistsException:
        return ApiResponse(status="error", message="Chat username already exists")

    return ApiResponse(status="ok", message="Chat updated successfully")


@chat_router.delete("/{chat_id}")
async def delete_chat(
    chat_id: UUID,
    chat_repo: ChatRepository = Depends(get_repo(ChatRepository)),
    user: User = Depends(get_current_user),
):
    """Delete a chat by its ID.

    Args:
        chat_id (UUID): The ID of the chat to delete.
        chat_repo (ChatRepository): The repository for chat operations.

    Returns:
        ApiResponse: The response indicating the result of the deletion operation.
    """
    chat = await chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chat not found"
        )
    if chat.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You are not the owner of this chat",
        )

    await chat_repo.delete_chat(chat_id)

    return ApiResponse(status="ok", message="Chat deleted successfully")
