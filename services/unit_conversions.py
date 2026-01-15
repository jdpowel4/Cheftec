import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

UNIT_CONVERSIONS = {
    # Weight and Mass
    ("oz", "lb"): Decimal("0.0625"),
    ("lb", "lb"): Decimal("1.0"),

    # Volume
    #("qt", "gal"): 0.25,
    #("pt", "qt"): 0.5,
    

    # Volume to Mass
    ("cup", "lb"): Decimal("0.55"),
    ("tbsp", "lb"): Decimal("0.034"),
    ("tsp", "lb"): Decimal("0.011"),
}

def convert(quantity, from_unit, to_unit):
    key = (from_unit.lower(), to_unit.lower())
    if key not in UNIT_CONVERSIONS:
        raise ValueError(f"No conversion from {from_unit} -> {to_unit}")
    return quantity * UNIT_CONVERSIONS[key]