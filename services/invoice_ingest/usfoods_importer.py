import logging
import csv
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime

from .base_importer import BaseInvoiceImporter
from .schemas import NormalizedInvoice, NormalizedInvoiceLineItem

logger = logging.getLogger(__name__)

class USFoodsInvoiceImporter(BaseInvoiceImporter):
    def load(self, file_path: str) -> NormalizedInvoice:
        line_items = []
        invoice_number = None
        invoice_date = None
        invoice_total = None

        logger.info(
            "Starting invoice import",
            extra={
                "vendor": "US Foods",
                "file": file_path
            }
        )

        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:

                if invoice_number is None:
                    invoice_number = row["DocumentNumber"].strip()
                    invoice_date = datetime.strptime(row["DocumentDate"].strip(), "%m/%d/%Y").date()
                    invoice_total = Decimal(row["NetAmountAfter Adjustment"])

                    logger.info(
                        "Invoice header parsed",
                        extra={
                            "vendor": "US Foods",
                            "invoice_number": invoice_number,
                            "invoice_date": invoice_date
                        }
                    )
                
                item = NormalizedInvoiceLineItem(
                    vendor_sku=row["ProductNumber"].strip(),
                    description=row["ProductDescription"].strip(),
                    quantity=Decimal(row["QtyShip"]),
                    unit=row["PricingUnit"],
                    unit_price=Decimal(row["UnitPrice"]),
                    extended_price=Decimal(row["ExtendedPrice"])
                    )
                
                logger.debug(
                     "Parsed line item",
                     extra={
                          "sku": item.vendor_sku,
                          "qty": str(item.quantity),
                          "unit": item.unit,
                          "price": str(item.unit_price)
                     }
                )

                calculated = (item.quantity * item.unit_price).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

                # Allow small rounding variance
                if calculated != item.extended_price:
                    logger.warning(
                         "Catch-weight pricing detected",
                         extra={
                              "sku": item.vendor_sku,
                              "qty": str(item.quantity),
                              "unit_price": str(item.unit_price),
                              "extended": str(item.extended_price)
                         }
                    )
                    # Likely a catch-weight or weight-based item
                    # Do NOT fail ingestion
                    print(
                        f"[INFO] Catch-weight pricing detected for SKU {item.vendor_sku}: "
                        f"{item.quantity} x {item.unit_price} ≠ {item.extended_price}"
                    )
                    item_is_weight_based = True
                else:
                    item_is_weight_based = False
                
                line_items.append(item)
                
        return NormalizedInvoice(
            vendor_name="US Foods",
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            total=invoice_total,
            line_items=line_items
        )