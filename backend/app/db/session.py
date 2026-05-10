"""SQLAlchemy engine and session configuration."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./fake_commerce.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Yield a database session and close it when done."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
