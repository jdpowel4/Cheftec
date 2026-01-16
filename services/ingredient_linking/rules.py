from models.ingredient import Ingredient

def exact_name_match(db, vendor_item):
    if not vendor_item.vendor_description:
        return []
    
    return (
        db.query(Ingredient)
        .filter(
            Ingredient.name.ilike(
                f"%{vendor_item.vendor_description}%"
            )
        )
        .all()
    )

def vendor_sku_match(db, vendor_item):
    return (
        db.query(Ingredient)
        .join(Ingredient.vendor_items)
        .filter(
            vendor_item.vendor_sku == vendor_item.vendor_sku
        )
        .all()
    )

ALL_RULES = [
    exact_name_match,
    vendor_sku_match
]