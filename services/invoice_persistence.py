from sqlalchemy.orm import Session
from decimal import Decimal

from models.vendor import Vendor
from models.invoice import Invoice, InvoiceLineItem
from models.vendor_item import VendorItem
from services.invoice_ingest.schemas import NormalizedInvoice

def persist_invoice(db: Session, invoice_data: NormalizedInvoice) -> Invoice:
    """
    Persist a normalized invoice into the database.
    """

    # Get or Create Vendor
    vendor = (
        db.query(Vendor)
        .filter(Vendor.name == invoice_data.vendor_name)
        .one_or_none()
    )

    if not vendor:
        vendor = Vendor(name=invoice_data.vendor_name)
        db.add(vendor)
        db.flush() # Get vendor ID

    # Create Invoice
    invoice = Invoice(
        vendor_id = vendor.id,
        invoice_number = invoice_data.invoice_number,
        invoice_date = invoice_data.invoice_date,
        total = invoice_data.total
    )
    db.add(invoice)
    db.flush() # Get Invoice ID

    # Process Line Items
    for item in invoice_data.line_items:

        # Get or create vendor item
        vendor_item = (
            db.query(VendorItem)
            .filter(
                VendorItem.vendor_id == vendor.id,
                VendorItem.vendor_sku == item.vendor_sku
            )
            .one_or_none()
        )

        if not vendor_item:
            vendor_item = VendorItem(
                vendor_id = vendor.id,
                vendor_sku = item.vendor_sku,
                vendor_description = item.description,
                purchase_unit = item.unit,
                unit_cost = item.unit_price
            )
            db.add(vendor_item)
            db.flush()

        line = InvoiceLineItem(
            invoice_id = invoice.id,
            vendor_item_id = vendor_item.id,
            quantity = item.quantity,
            unit_cost = item.unit_price,
            extended_cost=item.extended_price
        )
        db.add(line)
    db.commit()

    return invoice