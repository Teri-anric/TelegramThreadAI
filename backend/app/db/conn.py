from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import DATABASE_URL

def get_async_engine(url: str = DATABASE_URL) -> AsyncEngine:
    return create_async_engine(url)

async def get_async_session(engine = None) -> AsyncSession:
    if engine is None:
        engine = get_async_engine()
    
    async_session = async_sessionmaker(
        engine, 
        expire_on_commit=False,
        class_=AsyncSession
    )
    
    return async_session()
