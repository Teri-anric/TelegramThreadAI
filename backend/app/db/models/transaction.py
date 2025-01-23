"""
Database model for financial transactions.

This module defines the SQLAlchemy model for representing
financial transactions in the application's database schema.
"""

from sqlalchemy import UUID, Column, ForeignKey, Integer

from app.db.models.base import Base


class Transaction(Base):
    """
    Database model for transactions.
    """

    __tablename__ = "transactions"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    source_wallet_id = Column(UUID, ForeignKey("wallets.id"), nullable=False)
    destination_wallet_id = Column(UUID, ForeignKey("wallets.id"), nullable=False)

    source_amount = Column(Integer, nullable=False, default=0)
    destination_amount = Column(Integer, nullable=False, default=0)
