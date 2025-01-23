from sqlalchemy import Column, Integer, ForeignKey, UUID
import uuid
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
