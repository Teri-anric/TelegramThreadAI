"""
User-related API endpoints for the web application.
"""

from fastapi import APIRouter, Depends

from app.db.models.user import User
from ..shemas.user import UserSchema
from ..depends import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/me", response_model=UserSchema)
async def get_current_user(user: User = Depends(get_current_user)):
    """
    Get the current user's information.

    Returns: The current user's information.
    """
    return user
