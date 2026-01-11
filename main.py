from core.database import engine
from models import ingredient, vendor, vendor_item, invoice, inventory

ingredient.Base.metadata.create_all(bind=engine)
