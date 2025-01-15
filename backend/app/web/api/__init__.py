"""
API module.
"""

from fastapi import APIRouter

from .auth import router as auth_router
from .chat import router as chat_router

api_router = APIRouter(prefix="/api")

api_router.include_router(chat_router)
api_router.include_router(auth_router)
