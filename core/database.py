from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

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