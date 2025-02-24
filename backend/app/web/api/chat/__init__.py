"""
Chat API endpoints.
"""
from fastapi import APIRouter
from .crud import chat_crud_router
from .my import my_chats_router

chat_router = APIRouter(prefix="/chats")

chat_router.include_router(chat_crud_router)
chat_router.include_router(my_chats_router)

__all__ = ["chat_router"]
