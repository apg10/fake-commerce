"""SQLAlchemy database configuration for fake-commerce-backend."""

from backend.app.db.base import Base
from backend.app.db.session import SessionLocal, engine, get_db

__all__ = ["Base", "engine", "SessionLocal", "get_db"]
