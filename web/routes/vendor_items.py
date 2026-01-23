import logging
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.vendor_item import VendorItem
from models.vendor import Vendor
from services.vendor_item_service import get_unlinked_vendor_items
from starlette.templating import Jinja2Templates

logger = logging.getLogger(__name__)
router = APIRouter()
templates = Jinja2Templates(directory="web/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
 

@router.get("/vendor-items/unlinked")
def unlinked_vendor_items(
    request: Request,
    db: Session = Depends(get_db)
):
    
    items = get_unlinked_vendor_items(db)
    
    return templates.TemplateResponse(
        "vendor_items/unlinked.html",
        {
            "request": request,
            "vendor_items": items
        }
    )

@router.post("/vendor-items/{vendor_item_id}/link")
def link_vendor_item(
    vendor_item_id: int,
    ingredient_id: int = Form(...),
    db: Session = Depends(get_db)
):
    print(f"Linking vendor item {vendor_item_id} to ingredient {ingredient_id}.")  
    print("Attempting to fetch vendor item from database.")
    vi = db.get(VendorItem, vendor_item_id)
    print("Vendor item fetched:", vi)
    
    if not vi:
        print("Vendor item not found.")
        return
        
    vi.ingredient_id = ingredient_id
    db.commit()
    print("Vendor item linked and changes committed.")
    return HTMLResponse("""
    <tr style="opacity:0.4;">
      <td colspan="5"><em>Linked ✓</em></td>
    </tr>
    """)

"""
@router.post("/vendor-items/{vendor_item_id}/link")
def link_vendor_item(
    vendor_item_id: int,
    ingredient_id: int = Form(...),
    db: Session = Depends(get_db)
):
    print("🔥 LINK ROUTE HIT 🔥")
    print("Vendor Item:", vendor_item_id)
    print("Ingredient:", ingredient_id)
    return HTMLResponse("<div>LINKED</div>")
"""