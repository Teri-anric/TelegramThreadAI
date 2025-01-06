from app.db.repos import BaseRepository
from app.db.conn import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_repo(repo_type: type[BaseRepository], *args, **kwargs):
    def get_repo_func(session = Depends(get_async_session)):
        return repo_type(session, *args, **kwargs)

    return get_repo_func
