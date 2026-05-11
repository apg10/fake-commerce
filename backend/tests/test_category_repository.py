"""Tests for the category repository using an in-memory SQLite database."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.models.category import Category
from backend.app.repositories.category_repository import (
    create_category,
    get_category,
    list_categories,
)


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database and session for testing."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_create_category_persists_category(db_session: Session):
    """create_category persists a Category row."""
    category_data = {
        "name": "Electronics",
        "description": "Electronic devices and accessories",
    }
    category = create_category(db_session, category_data)
    assert category.id is not None
    assert category.name == "Electronics"
    assert category.description == "Electronic devices and accessories"
    assert category.is_active is True


def test_list_categories_returns_created_categories(db_session: Session):
    """list_categories returns a list containing the created categories."""
    data_one = {"name": "Books"}
    data_two = {"name": "Clothing"}

    create_category(db_session, data_one)
    create_category(db_session, data_two)

    categories = list_categories(db_session)
    assert len(categories) == 2
    names = {c.name for c in categories}
    assert {"Books", "Clothing"}.issubset(names)


def test_get_category_returns_existing_category(db_session: Session):
    """get_category returns an existing category by ID."""
    category = create_category(db_session, {"name": "Toys", "description": "Toys and games"})
    fetched = get_category(db_session, category.id)

    assert fetched is not None
    assert fetched.id == category.id
    assert fetched.name == "Toys"


def test_get_category_returns_none_for_unknown_category(db_session: Session):
    """get_category returns None when no category matches the given ID."""
    fetched = get_category(db_session, 9999)
    assert fetched is None
