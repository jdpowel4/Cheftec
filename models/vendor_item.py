from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from core.database import Base
from models.base import TimestampMixin

class VendorItem(Base, TimestampMixin):
    __tablename__ = "vendor_items"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    ingredient_id = Column(Integer, ForeignKey("ingredients.id"), nullable=False)

    vendor_sku = Column(String, nullable=False)
    pack_size = Column(String, nullable=True)   # "6 x 2Lb"
    unit_cost = Column(Numeric(10, 2), nullable=False)

    vendor = relationship("Vendor")
    ingredient = relationship("Ingredient")
