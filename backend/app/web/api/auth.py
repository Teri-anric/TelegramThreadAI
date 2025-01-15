"""
Authentication API endpoints.
"""

from app.db.repos.user import UserRepository
from app.utils.access_token import create_access_token
from app.utils.telegram_login import verify_telegram_login
from app.web.depends import get_repo
from fastapi import APIRouter, Depends, HTTPException

from .shemas.user import LoginData, LoginResponse, UserSchema

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login", response_model=LoginResponse, status_code=200)
async def login(
    login_data: LoginData, user_repo: UserRepository = Depends(get_repo(UserRepository))
):
    """
    Authenticate a user via Telegram login
    """
    if login_data.login_type != "tg_login_widget":
        raise HTTPException(status_code=400, detail="Invalid login type")

    if not verify_telegram_login(login_data.credentials.model_dump()):
        raise HTTPException(status_code=400, detail="Invalid Telegram login data")

    user = await user_repo.create_or_update_user(
        login_data.credentials.id,
        first_name=login_data.credentials.first_name,
        last_name=login_data.credentials.last_name,
        username=login_data.credentials.username,
        photo_url=login_data.credentials.photo_url,
    )
    # Generate tokens on the fly
    payload = {"sub": user.telegram_id}
    access_token = create_access_token(payload)

    return LoginResponse(status="ok", user=user, access_token=access_token)


@router.get("/profile", response_model=UserSchema)
async def get_profile(
    user_id: int, user_repo: UserRepository = Depends(get_repo(UserRepository))
):
    """
    Get the current user's profile
    """
    user = await user_repo.get_user_by_telegram_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
