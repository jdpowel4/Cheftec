def link_vendor_item(
        db,
        vendor_item,
        ingredient,
        confidence: float
):
    vendor_item.ingredient_id = ingredient.id
    vendor_item.link_confidence = confidence
    db.commit()