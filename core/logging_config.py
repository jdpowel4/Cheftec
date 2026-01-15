import logging
from logging.handlers import RotatingFileHandler
import sys

from . import settings

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

def configure_logging():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[
            RotatingFileHandler(
                "app.log",
                maxBytes=5_000_000,
                backupCount=5
            ),
            logging.StreamHandler(sys.stdout)
        ]
    )