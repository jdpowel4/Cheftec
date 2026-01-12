from abc import ABC, abstractmethod
from .schemas import NormalizedInvoice

class BaseInvoiceImporter(ABC):

    @abstractmethod
    def load(self, file_path: str) -> NormalizedInvoice:
        """Load and normalized an invoice file"""
        pass