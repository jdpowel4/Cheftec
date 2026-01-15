import logging
logger = logging.getLogger(__name__)

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)

    transaction_type = Column(String, nullable=False)   # IN, OUT, ADJUST
    quantity = Column(Numeric(10, 4), nullable=False)
    unit = Column(String, nullable=False)

    reference_type = Column(String, nullable=True)
    reference_id = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ingredient = relationship("Ingredient")