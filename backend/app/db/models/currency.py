"""
Database model for currencies.

This module defines the SQLAlchemy model for representing
currency information in the application's database schema.
"""

import uuid

from sqlalchemy import UUID, Column, Integer, String

from app.db.models.base import Base


class Currency(Base):
    """
    Database model for currencies.
    """

    __tablename__ = "currencies"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    code = Column(String, nullable=False)

    decimal = Column(Integer, nullable=False, default=2)
