"""
Chat message API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from uuid import UUID

from app.db.models.user import User
from app.db.repos.chat import ChatRepository
from app.db.repos.chat_member import ChatMemberRepository
from app.db.repos.message import MessageRepository
from app.web.depends import get_current_user, get_repo
from app.web.shemas.chat_messages import PaginatedChatMessagesResponse, ChatMessageResponse

chat_messages_router = APIRouter(prefix="/messages", tags=["Chat Messages"])


@chat_messages_router.get(
    "/{chat_id}",
    response_model=PaginatedChatMessagesResponse,
    summary="Get chat messages",
    description="Retrieve paginated messages for a specific chat.",
)
async def get_chat_messages(
    chat_id: UUID = Path(..., description="Unique identifier of the chat"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(50, ge=1, le=100, description="Number of messages per page"),
    user: User = Depends(get_current_user),
    chat_repo: ChatRepository = Depends(get_repo(ChatRepository)),
    chat_member_repo: ChatMemberRepository = Depends(get_repo(ChatMemberRepository)),
    message_repo: MessageRepository = Depends(get_repo(MessageRepository))
):
    """
    Retrieve paginated messages for a specific chat.

    Requires the user to be a member of the chat.
    """
    # Check if chat exists
    chat = await chat_repo.get_chat_by_id(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    # Check if user is a member of the chat
    chat_member = await chat_member_repo.get_chat_member(chat_id, user.id)
    if not chat_member:
        raise HTTPException(status_code=403, detail="Not a member of this chat")

    # Get paginated messages
    paginated_messages = await message_repo.get_messages_by_chat(
        chat_id=chat_id, page=page, per_page=per_page
    )

    # Convert to response model
    return PaginatedChatMessagesResponse(
        items=[
            ChatMessageResponse.model_validate(message) 
            for message in paginated_messages.items
        ],
        total_items=paginated_messages.total_items,
        total_pages=paginated_messages.total_pages,
        page=paginated_messages.page,
        per_page=paginated_messages.per_page,
        has_next=paginated_messages.has_next,
        has_previous=paginated_messages.has_previous,
        next_page=paginated_messages.next_page,
        previous_page=paginated_messages.previous_page
    ) 