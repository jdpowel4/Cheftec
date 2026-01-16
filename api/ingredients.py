@router.post("\ingredients\bulk")
def bulk_create(payload: BulkIngredientCreate, db=Depends(get_db)):
    return bulk_create_ingredients(db, payload.names)
