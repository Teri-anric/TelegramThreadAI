"""
Database connection module.
"""

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from app.config import DATABASE_URL


def get_async_engine(url: str = DATABASE_URL) -> AsyncEngine:
    """
    Get an async engine for the database.
    """
    return create_async_engine(url)


async def get_async_session(engine=None) -> AsyncSession:
    """
    Get an async session for the database.
    """
    if engine is None:
        engine = get_async_engine()

    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session()
