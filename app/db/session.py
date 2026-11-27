from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import DATABASE_URL, STORAGE_BACKEND


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session | None, None, None]:
    if STORAGE_BACKEND != "mysql":
        yield None
        return

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()