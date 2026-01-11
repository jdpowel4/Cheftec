from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship

from core.database import Base
from models.base import TimestampMixin

class Recipe(Base, TimestampMixin):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    yield_quantity = Column(Numeric(10, 4), nullable=False)
    yield_unit = Column(String, nullable=False)

    ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )