import csv
from decimal import Decimal
from datetime import datetime

from .base_importer import BaseInvoiceImporter
from .schemas import NormalizedInvoice, NormalizedInvoiceLineItem

class PFSInvoiceImporter(BaseInvoiceImporter):
    def load(self, file_path: str) -> NormalizedInvoice:
        line_items = []
        invoice_number = None
        invoice_date = None

        with open(file_path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                if not invoice_number:
                    invoice_number = row["Invoice Number"]
                    invoice_date = datetime.strptime(row["Invoice Date"], "%m/%d/%Y").date()
                
                line_items.append(
                    NormalizedInvoiceLineItem(
                        vendor_sku=row["Product #"].strip(),
                        description=row["Product Description"].strip(),
                        quantity=Decimal(row["Qty Shipped"]),
                        unit=row["UOM"],
                        unit_price=Decimal(row["Unit Price"]),
                        extended_price=Decimal(row["Ext. Price"])
                    )
                )
        return NormalizedInvoice(
            vendor_name="PFS",
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            line_items=line_items
        )
