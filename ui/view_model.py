from services.vendor_item_service import get_unlinked_vendor_items
from services.ingredient_linking.engine import suggest_ingredient_links
from services.ingredient_linking.linker import link_vendor_item

class IngredientLinkingViewModel:
    def __init__(self, db):
        self.db = db
    
    def load_unlinked_items(self):
        return get_unlinked_vendor_items(self.db)
    
    def get_suggestions(self, vendor_item):
        return suggest_ingredient_links(self.db, vendor_item)
    
    def link(self, vendor_item, ingredient, confidence):
        link_vendor_item(
            self.db,
            vendor_item,
            ingredient,
            confidence
        )