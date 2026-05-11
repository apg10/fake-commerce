"""Tests for the category repository using an in-memory SQLite database."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.models.category import Category
from backend.app.repositories.category_repository import (
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
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


def test_update_category_updates_one_field(db_session: Session):
    """update_category updates one field only."""
    category = create_category(db_session, {"name": "Original Name", "description": "Original desc"})
    updated = update_category(db_session, category.id, {"name": "New Name"})

    assert updated is not None
    assert updated.name == "New Name"
    assert updated.description == "Original desc"
    assert updated.is_active is True


def test_update_category_updates_multiple_fields(db_session: Session):
    """update_category updates multiple fields in one call."""
    category = create_category(db_session, {"name": "Name", "description": "Desc", "is_active": True})
    updated = update_category(db_session, category.id, {"name": "Updated", "description": "Updated desc", "is_active": False})

    assert updated is not None
    assert updated.name == "Updated"
    assert updated.description == "Updated desc"
    assert updated.is_active is False


def test_update_category_empty_dict_preserves_values(db_session: Session):
    """update_category with empty dict preserves existing values."""
    category = create_category(db_session, {"name": "Preserved", "description": "Kept", "is_active": True})
    updated = update_category(db_session, category.id, {})

    assert updated is not None
    assert updated.name == "Preserved"
    assert updated.description == "Kept"
    assert updated.is_active is True


def test_update_category_returns_none_for_unknown_category(db_session: Session):
    """update_category returns None for unknown category ID."""
    result = update_category(db_session, 9999, {"name": "Ghost"})
    assert result is None


def test_delete_category_deletes_and_returns_true(db_session: Session):
    """delete_category deletes an existing category and returns True."""
    category = create_category(db_session, {"name": "Delete Me"})
    result = delete_category(db_session, category.id)

    assert result is True


def test_delete_category_returns_false_for_unknown_category(db_session: Session):
    """delete_category returns False for unknown category ID."""
    result = delete_category(db_session, 9999)
    assert result is False


def test_deleted_category_not_returned_by_get_category(db_session: Session):
    """After deletion, get_category returns None for the deleted category."""
    category = create_category(db_session, {"name": "Gone", "description": "Deleted"})
    delete_category(db_session, category.id)

    fetched = get_category(db_session, category.id)
    assert fetched is None


def test_deleting_one_category_does_not_delete_another(db_session: Session):
    """Deleting one category does not affect another category."""
    keep = create_category(db_session, {"name": "Keep", "description": "Stay"})
    remove = create_category(db_session, {"name": "Remove", "description": "Go away"})

    delete_category(db_session, remove.id)

    still_there = get_category(db_session, keep.id)
    assert still_there is not None
    assert still_there.name == "Keep"

    gone = get_category(db_session, remove.id)
    assert gone is None
