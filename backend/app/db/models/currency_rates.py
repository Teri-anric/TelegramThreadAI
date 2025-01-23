from sqlalchemy import Column, Integer, ForeignKey, Numeric, UUID
import uuid
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
