import logging
from services.unit_conversions import convert
from decimal import Decimal

logger = logging.getLogger(__name__)

def calculate_recipe_cost(recipe):
    total_cost = Decimal(0)

    for ri in recipe.ingredients:
        ingredient = ri.ingredient

        # Convert recipe unit -> ingredient base unit
        qty_in_base = convert(
            ri.quantity,
            ri.unit,
            ingredient.base_unit
        )

        line_cost = qty_in_base * ingredient.current_cost_per_base_unit
        total_cost += line_cost
    
    return total_cost.quantize(Decimal("0.0001"))

def cost_per_portion(recipe):
    total_cost = calculate_recipe_cost(recipe)
    return round(total_cost / float(recipe.yield_quantity), 4)
