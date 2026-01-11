from sqlalchemy import Column, Integer, String
from core.database import Base
from models.base import TimestampMixin

class Vendor(Base, TimestampMixin):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)