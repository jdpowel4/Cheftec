from core.database import SessionLocal
from core.logging_config import configure_logging
from services.invoice_ingest.usfoods_importer import USFoodsInvoiceImporter
from services.invoice_ingest.pfs_importer import PFSInvoiceImporter
from services.invoice_persistence import persist_invoice
from uuid import uuid4

configure_logging()
db = SessionLocal()

us_invoice = USFoodsInvoiceImporter().load(r"C:\Users\Jeremy Powell\Downloads\InvoiceDetails (6).csv")
persist_invoice(db, us_invoice, ingest_id=str(uuid4()))

pfs_invoice = PFSInvoiceImporter().load(r"C:\Users\Jeremy Powell\Downloads\CustomerFirstInvoiceExport_20260115002224.csv")
persist_invoice(db, pfs_invoice, ingest_id=str(uuid4()))

print("Smoke-Test Passed")