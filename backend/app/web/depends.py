"""
Dependency functions for the backend.
"""

from fastapi import Depends, HTTPException, Request

from app.db.conn import get_async_session
from app.db.models.user import User
from app.db.repos import BaseRepository
from app.db.repos.user import UserRepository
from app.utils.access_token import decode_token


def get_repo(repo_type: type[BaseRepository], *args, **kwargs):
    """
    Get a dependency function for a repository instance.
    """

    def get_repo_func():
        """
        Create a repository instance.
        """
        session = get_async_session()
        return repo_type(session, *args, **kwargs)

    return get_repo_func


async def get_current_user(
    request: Request, user_repo: UserRepository = Depends(get_repo(UserRepository))
) -> User:
    """
    Get the current user from the request.
    """
    # Get the token from the request
    token = request.headers.get("Authorization") or request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # check shema
    if not token.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    # Remove the "Bearer " prefix
    token = token.removeprefix("Bearer ")
    if not token:
        raise HTTPException(status_code=401, detail="Token is empty")
    # Decode the token
    payload = decode_token(token)
    user_id = payload["sub"]
    # Get the user by id
    user = await user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
