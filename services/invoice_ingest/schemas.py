import logging
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import List, Optional

logger = logging.getLogger(__name__)

@dataclass
class NormalizedInvoiceLineItem:
    vendor_sku: str
    description: str
    quantity: Decimal
    unit: str
    unit_price: Decimal
    extended_price: Decimal

@dataclass
class NormalizedInvoice:
    vendor_name: str
    invoice_number: str
    invoice_date: date
    total: Decimal
    line_items: List[NormalizedInvoiceLineItem]