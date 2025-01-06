from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from sqlalchemy import Column, MetaData
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    metadata = MetaData()

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
