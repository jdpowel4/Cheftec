import uuid
import logging

from services.invoice_persistence import persist_invoice

logger = logging.getLogger(__name__)

def ingest_invoice(importer, file_path, db):
    ingest_id = str(uuid.uuid4())

    logger.info(
        "Starting invoice ingest",
        extra={"ingest_id": ingest_id}
    )

    invoice_data = importer.load(file_path)

    invoice = persist_invoice(
        db,
        invoice_data,
        ingest_id=ingest_id
    )

    logger.info(
        "Invoice ingest completed",
        extra={
            "ingest_id": ingest_id,
            "invoice_number": invoice.invoice_number
        }
    )

    return invoice