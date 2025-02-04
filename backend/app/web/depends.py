"""
Dependency functions for the backend.
"""

from fastapi import Depends, HTTPException, Request

from app.db.conn import get_async_session
from app.db.models.user import User
from app.db.repos import BaseRepository
from app.db.repos.user import UserRepository
from app.utils.access_token import decode_token
from app.web.security import oauth2_scheme


def get_repo(repo_type: type[BaseRepository], *args, **kwargs):
    """
    Get a dependency function for a repository instance.
    """

    def get_repo_func():
        """
        Create a repository instance.
        """
        with get_async_session() as session:
            yield repo_type(session, *args, **kwargs)

    return get_repo_func


async def get_current_user_or_none(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(get_repo(UserRepository)),
) -> User | None:
    """
    Get the current user from the request.
    """
    # Decode the token
    payload = decode_token(token)
    user_id = payload["sub"]
    # Get the user by id
    return await user_repo.get_user_by_id(user_id)


async def get_current_user(
    user: User | None = Depends(get_current_user_or_none),
) -> User:
    """
    Get the current user from the request.
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
