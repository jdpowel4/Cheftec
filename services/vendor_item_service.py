import logging
from sqlalchemy.orm import Session
from models.vendor_item import VendorItem

logger = logging.getLogger(__name__)

def get_unlinked_vendor_items(
        db: Session,
        vendor_id: int | None = None
):
    query = db.query(VendorItem).filter(
        VendorItem.ingredient_id.is_(None)
    )

    if vendor_id:
        query = query.filter(VendorItem.vendor_id == vendor_id)

    return query.order_by(VendorItem.created_at.desc()).all()