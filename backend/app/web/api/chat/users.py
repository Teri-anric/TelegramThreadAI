# FIXME: This is a temporary solution to get the chat members and requests

from fastapi import Depends, HTTPException, Path, status

from . import chat_router
from app.db.models.chat_member import ChatMemberStatus
from app.db.models.user import User
from app.db.repos.chat_member import ChatMemberRepository
from app.web.depends import get_current_user, get_repo
from app.web.shemas.chat import (
    ChatMemberListResponse, 
    ChatRequestListResponse
)
from uuid import UUID

async def _check_chat_member_permission(
    chat_id: UUID, 
    user: User, 
    chat_member_repo: ChatMemberRepository,
    require_admin: bool = False
):
    """
    Helper function to check user's chat membership and permissions.
    
    :param chat_id: ID of the chat to check
    :param user: Current user
    :param chat_member_repo: Chat member repository
    :param require_admin: Whether admin/owner permissions are required
    :raises HTTPException: If chat not found or insufficient permissions
    """
    # Check if chat exists
    chat_member = await chat_member_repo.get_chat_member(chat_id, user.id)
    if not chat_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Chat not found or you are not a member"
        )

    # Check admin permissions if required
    if require_admin and chat_member.status not in [
        ChatMemberStatus.ADMIN, 
        ChatMemberStatus.OWNER
    ]:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, 
            detail="Insufficient permissions"
        )

@chat_router.get(
    "/{chat_id}/users/requests",
    response_model=ChatRequestListResponse,
    summary="Get chat join requests",
    description="Retrieve a list of join requests for a specific chat. Requires admin or owner permissions.",
    responses={
        400: {"description": "Not a chat member"},
        406: {"description": "Insufficient permissions"},
        404: {"description": "Chat not found"},
    },
)
async def get_chat_join_requests(
    chat_id: UUID = Path(..., description="ID of the chat"),
    user: User = Depends(get_current_user),
    chat_member_repo: ChatMemberRepository = Depends(get_repo(ChatMemberRepository))
):
    """
    Retrieve join requests for a specific chat.
    
    Requires admin or owner permissions.
    """
    # Check permissions first
    await _check_chat_member_permission(
        chat_id, user, chat_member_repo, require_admin=True
    )

    # Get join requests
    join_requests = await chat_member_repo.get_chat_join_requests(chat_id)
    return ChatRequestListResponse(requests=join_requests)

@chat_router.get(
    "/{chat_id}/users",
    response_model=ChatMemberListResponse,
    summary="Get chat members",
    description="Retrieve a list of members for a specific chat.",
    responses={404: {"description": "Chat not found"}},
)
async def get_chat_members(
    chat_id: UUID = Path(..., description="ID of the chat"),
    user: User = Depends(get_current_user),
    chat_member_repo: ChatMemberRepository = Depends(get_repo(ChatMemberRepository))
):
    """
    Retrieve members for a specific chat.
    """
    # Check if chat exists and user is a member
    await _check_chat_member_permission(chat_id, user, chat_member_repo)

    # Get chat members
    members = await chat_member_repo.get_chat_members(chat_id)
    return ChatMemberListResponse(members=members)

@chat_router.get(
    "/{chat_id}/users/banned",
    response_model=ChatMemberListResponse,
    summary="Get banned users",
    description="Retrieve a list of banned users for a specific chat. Requires admin or owner permissions.",
    responses={
        400: {"description": "Not a chat member"},
        406: {"description": "Insufficient permissions"},
        404: {"description": "Chat not found"},
    },
)
async def get_banned_users(
    chat_id: UUID = Path(..., description="ID of the chat"),
    user: User = Depends(get_current_user),
    chat_member_repo: ChatMemberRepository = Depends(get_repo(ChatMemberRepository))
):
    """
    Retrieve banned users for a specific chat.
    
    Requires admin or owner permissions.
    """
    # Check permissions first
    await _check_chat_member_permission(
        chat_id, user, chat_member_repo, require_admin=True
    )

    # Get banned members
    banned_members = await chat_member_repo.get_chat_banned_members(chat_id)
    return ChatMemberListResponse(members=banned_members)