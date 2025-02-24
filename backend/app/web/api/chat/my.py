from fastapi import Depends, APIRouter, Query
from app.db.models.user import User
from app.db.repos.chat_member import ChatMemberRepository
from app.web.depends import get_current_user, get_repo
from app.web.shemas.chat import ChatListResponse
from app.web.shemas.paginate import PaginationParams

my_chats_router = APIRouter(prefix="/my", tags=["My chats"])


@my_chats_router.get(
    "",
    response_model=ChatListResponse,
    summary="Get user's chats",
    description="Retrieve a list of chats the current user is a member of.",
)
async def get_user_chats(
    user: User = Depends(get_current_user),
    chat_member_repo: ChatMemberRepository = Depends(get_repo(ChatMemberRepository)),
    params: PaginationParams = Query(...)
):
    """
    Retrieve the list of chats the current user is a member of.
    
    Returns:
        ChatListResponse: A list of chats the user belongs to.
    """
    chats = await chat_member_repo.get_user_active_chats(
        user_id=user.id, 
        page=params.page,
        per_page=params.per_page
    )
    return ChatListResponse.model_validate(chats)

@my_chats_router.get(
    "/requests",
    response_model=ChatListResponse,
    summary="Get user's chat requests",
    description="Retrieve a list of chats where the current user has a pending join request.",
)
async def get_user_chat_requests(
    user: User = Depends(get_current_user),
    chat_member_repo: ChatMemberRepository = Depends(get_repo(ChatMemberRepository)),
    params: PaginationParams = Query(...)
):
    """
    Retrieve the list of chats where the current user has a pending join request.
    
    Returns:
        ChatListResponse: A list of chats with pending join requests.
    """
    chat_requests = await chat_member_repo.get_user_pending_chats(
        user_id=user.id, 
        page=params.page,
        per_page=params.per_page
    )
    return ChatListResponse.model_validate(chat_requests)
