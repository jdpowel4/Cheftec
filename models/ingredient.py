from sqlalchemy import Column, Integer, String
from core.database import Base
from models.base import TimestampMixin

class Ingredient(Base, TimestampMixin):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    base_unit = Column(String, nullable=False)  #Lb, oz, each, etc