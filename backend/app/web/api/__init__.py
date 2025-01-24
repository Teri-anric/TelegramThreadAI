"""
API module.
"""

from fastapi import APIRouter

from .auth import auth_router
from .chat import chat_router
from .user import user_router

api_router = APIRouter(prefix="/api")

api_router.include_router(chat_router)
api_router.include_router(auth_router)
api_router.include_router(user_router)

__all__ = ["api_router"]
