from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from core.database import Base
from models.base import TimestampMixin

class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    base_unit = Column(String, nullable=False)  #Lb, oz, each, etc
    current_cost_per_base_unit = Column(Numeric(10, 4), nullable=True)

    vendor_items = relationship("VendorItem", back_populates="ingredient")