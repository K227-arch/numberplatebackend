from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

from typing import Generator

from app.core.settings import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=0
)

sessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_session() -> Generator:
    session = sessionLocal()
    try:
        yield session
    finally:
        session.close()

