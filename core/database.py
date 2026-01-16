import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///./cheftec.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}   #SQLite Only
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)

Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()