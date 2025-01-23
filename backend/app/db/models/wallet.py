import enum
import uuid
from sqlalchemy import UUID, Column, ForeignKey, Integer, Enum

from app.db.models.base import Base


class WalletType(enum.Enum):
    """Enum for wallet type."""
    EXTERNAL = "external"
    INTERNAL = "internal"


class Wallet(Base): 
    """
    Database model for user wallets.
    NOT RELATED TO USER CHAT AND OTHER MODELS
    """

    __tablename__ = "wallets"

    id = Column(UUID, primary_key=True, index=True, default=uuid.uuid4)

    currency_id = Column(UUID, ForeignKey("currencies.id"), nullable=False)
    type = Column(Enum(WalletType), default=WalletType.INTERNAL, nullable=False)

    balance = Column(Integer, nullable=False, default=0)

    user_id = Column(UUID, ForeignKey("users.id"), nullable=True)
    chat_id = Column(UUID, ForeignKey("chats.id"), nullable=True)
