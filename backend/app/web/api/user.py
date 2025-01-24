from fastapi import APIRouter, Depends

from app.db.models.user import User
from app.web.api.shemas.user import UserSchema
from app.web.depends import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/me", response_model=UserSchema)
async def get_current_user(user: User = Depends(get_current_user)):
    return user
