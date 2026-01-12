import csv
from decimal import Decimal

from .base_importer import BaseInvoiceImporter
from .schemas import NormalizedInvoice, NormalizedInvoiceLineItem

class USFoodsInvoiceImporter(BaseInvoiceImporter):
    def load(self, file_path: str) -> NormalizedInvoice:
        line_items = []

        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                item = NormalizedInvoiceLineItem(
                    vendor_sku=row["ProductNumber"].strip(),
                    description=row["ProductDescription"].strip(),
                    quantity=Decimal(row["QtyShip"]),
                    unit=row["PricingUnit"],
                    unit_price=Decimal(row["UnitPrice"]),
                    extended_price=Decimal(row["ExtendedPrice"])
                    )
                
                calculated = (item.quantity * item.unit_price).quantize(Decimal("0.01"))

                if calculated != item.extended_price:
                    raise ValueError(
                        f"Invoice math mismatch for SKU {item.vendor_sku}:"
                        f"{item.quantity} x {item.unit_price} = {calculated},"
                        f"CSV says {item.extended_price}"
                    )
                
                line_items.append(item)
                
        return NormalizedInvoice(
            vendor_name="US Foods",
            invoice_number=row["DocumentNumber"],
            invoice_date=row["DocumentDate"],
            line_items=line_items
        )