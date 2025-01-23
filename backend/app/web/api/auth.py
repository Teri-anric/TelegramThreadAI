"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException

from app.db.repos.user import UserRepository
from app.utils.access_token import create_access_token
from app.utils.telegram_login import verify_telegram_login
from app.web.depends import get_repo

from .shemas.login import LoginData, LoginResponse, UserSchema

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/login", response_model=LoginResponse, status_code=200)
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
    payload = {"sub": user.id}
    access_token = create_access_token(payload)

    return LoginResponse(status="ok", user=user, access_token=access_token)
