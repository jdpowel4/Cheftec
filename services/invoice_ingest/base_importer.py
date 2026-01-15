import logging
from abc import ABC, abstractmethod
from .schemas import NormalizedInvoice

logger = logging.getLogger(__name__)

class BaseInvoiceImporter(ABC):
    vendor_name = "UNKNOWN"

    @abstractmethod
    def load(self, file_path: str) -> NormalizedInvoice:
        """Load and normalized an invoice file"""
        raise NotImplementedError