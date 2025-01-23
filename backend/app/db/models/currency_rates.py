"""
Database model for currency exchange rates.

This module defines the SQLAlchemy model for representing
currency exchange rates in the application's database schema.
"""

import uuid

from sqlalchemy import UUID, Column, ForeignKey, Numeric

from app.db.models.base import Base


class CurrencyRate(Base):
    """
    Database model for currency rates.
    """

    __tablename__ = "currency_rates"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    source_currency_id = Column(UUID, ForeignKey("currencies.id"), nullable=False)
    destination_currency_id = Column(UUID, ForeignKey("currencies.id"), nullable=False)

    rate = Column(Numeric, nullable=False, default=0)
