import logging
from sqlalchemy.orm import Session
from decimal import Decimal

from models.vendor import Vendor
from models.invoice import Invoice, InvoiceLineItem
from models.vendor_item import VendorItem
from services.invoice_ingest.schemas import NormalizedInvoice


logger = logging.getLogger(__name__)

def persist_invoice(db: Session, invoice_data: NormalizedInvoice, ingest_id: str) -> Invoice:
    """
    Persist a normalized invoice into the database.
    """

    logger.info(
        "Persisting invoice",
        extra={
            "ingest_id": ingest_id,
            "vendor": invoice_data.vendor_name,
            "invoice_number": invoice_data.invoice_number,
            "total": str(invoice_data.total),
            "line_items": len(invoice_data.line_items)
        }
    )

    # Get or Create Vendor
    vendor = (
        db.query(Vendor)
        .filter(Vendor.name == invoice_data.vendor_name)
        .one_or_none()
    )

    existing = (
        db.query(Invoice)
        .filter(
            Invoice.vendor_id == vendor.id,
            Invoice.invoice_number == invoice_data.invoice_number
        )
        .one_or_none()
    )

    if existing:
        logger.warning(
            "Duplicate invoice detected - skipping insert",
            extra={
                "ingest_id": ingest_id,
                "vendor_id": vendor.id,
                "invoice_number": invoice_data.invoice_number,
                "invoice_id": existing.id
            }
        )
        return existing

    if not vendor:
        vendor = Vendor(name=invoice_data.vendor_name)
        db.add(vendor)
        db.flush() # Get vendor ID

    total = sum(
        item.extended_price
        for item in invoice_data.line_items
    )
    # Create Invoice
    invoice = Invoice(
        vendor_id = vendor.id,
        invoice_number = invoice_data.invoice_number,
        invoice_date = invoice_data.invoice_date,
        total = total
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
            logger.info(
                "Creating Vendor Item",
                extra={
                    "ingest_id": ingest_id,
                    "vendor_id": vendor.id,
                    "sku": item.vendor_sku,
                    "unit": item.unit
                }
            )
            vendor_item = VendorItem(
                vendor_id = vendor.id,
                vendor_sku = item.vendor_sku,
                vendor_description = item.description,
                purchase_unit = item.unit,
                unit_cost = item.unit_price
            )
            db.add(vendor_item)
            db.flush()

        if vendor_item.ingredient_id is None:
            logger.warning(
                "Vendor item not linked to ingredient yet",
                extra={
                    "ingest_id": ingest_id,
                    "vendor": vendor.name,
                    "vendor_sku": vendor_item.vendor_sku,
                    "description": vendor_item.vendor_description
                }
            )
        line = InvoiceLineItem(
            invoice_id = invoice.id,
            vendor_item_id = vendor_item.id,
            quantity = item.quantity,
            unit_cost = item.unit_price,
            extended_cost=item.extended_price
        )
        db.add(line)

        assert invoice.total is not None
        assert invoice.total >= 0
        
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    return invoice