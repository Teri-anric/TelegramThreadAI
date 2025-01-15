"""
Dependency functions for the backend.
"""

from fastapi import Depends

from app.db.conn import get_async_session
from app.db.repos import BaseRepository


def get_repo(repo_type: type[BaseRepository], *args, **kwargs):
    """
    Get a dependency function for a repository instance.
    """

    def get_repo_func(session=Depends(get_async_session)):
        """
        Create a repository instance.
        """
        return repo_type(session, *args, **kwargs)

    return get_repo_func
