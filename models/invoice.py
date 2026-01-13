from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from core.database import Base
from models.base import TimestampMixin

class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    invoice_number = Column(String, nullable=False)
    invoice_date = Column(Date, nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    vendor = relationship("Vendor")
    line_items = relationship("InvoiceLineItem", back_populates="invoice")

class InvoiceLineItem(Base):
    __tablename__ = "invoice_line_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    vendor_item_id = Column(Integer, ForeignKey("vendor_items.id"), nullable=False)

    quantity = Column(Numeric(10, 4), nullable=False)
    unit_cost = Column(Numeric(10, 4), nullable=False)
    extended_cost = Column(Numeric(10, 4), nullable=False)

    invoice = relationship("Invoice", back_populates="line_items")
    vendor_item = relationship("VendorItem")