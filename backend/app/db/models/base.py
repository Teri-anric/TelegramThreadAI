"""
Module for the base model.
"""

from sqlalchemy import Column, DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """
    Base model for all database models.
    """

    metadata = MetaData()

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
