"""Smoke tests for the database session module."""

from sqlalchemy import text

from backend.app.db.session import engine, SessionLocal, get_db


def test_session_module_exposes_engine_and_sessionlocal():
    assert engine is not None
    assert SessionLocal is not None


def test_get_db_yields_usable_session():
    db = None
    gen = get_db()
    try:
        db = next(gen)
        assert db is not None
    finally:
        gen.close()


def test_simple_sql_statement_executes():
    db = None
    gen = get_db()
    try:
        db = next(gen)
        result = db.execute(text("SELECT 1"))
        assert result.fetchone()[0] == 1
    finally:
        gen.close()
