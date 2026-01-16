from sqlalchemy.orm import Session
from models.vendor_item import VendorItem
from .rules import ALL_RULES
from .scorer import score_matches

def suggest_ingredient_links(
        db: Session,
        vendor_item: VendorItem
):
    candidates = []

    for rule in ALL_RULES:
        matches = rule(db, vendor_item)
        candidates.extend(matches)
    
    return score_matches(candidates)
