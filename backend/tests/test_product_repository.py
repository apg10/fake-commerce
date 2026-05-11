"""Tests for the product repository using an in-memory SQLite database."""

from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.models.product import Product
from backend.app.repositories.product_repository import (
    create_product,
    delete_product,
    get_product,
    list_products,
    update_product,
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


def test_create_product_persists_product(db_session: Session):
    """create_product persists a Product row."""
    product_data = {
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse",
        "price": Decimal("29.99"),
        "stock": 100,
        "is_active": True,
    }
    product = create_product(db_session, product_data)
    assert product.id is not None
    assert product.name == "Wireless Mouse"
    assert product.description == "Ergonomic wireless mouse"
    assert product.price == Decimal("29.99")
    assert product.stock == 100
    assert product.is_active is True


def test_list_products_returns_created_products(db_session: Session):
    """list_products returns a list containing the created products."""
    data_one = {"name": "Keyboard", "price": Decimal("49.99"), "stock": 50}
    data_two = {"name": "Monitor", "price": Decimal("299.99"), "stock": 25}

    create_product(db_session, data_one)
    create_product(db_session, data_two)

    products = list_products(db_session)
    assert len(products) == 2
    names = {p.name for p in products}
    assert {"Keyboard", "Monitor"}.issubset(names)


def test_get_product_returns_existing_product(db_session: Session):
    """get_product returns an existing product by ID."""
    product = create_product(db_session, {"name": "USB Hub", "price": Decimal("19.99"), "stock": 200})
    fetched = get_product(db_session, product.id)

    assert fetched is not None
    assert fetched.id == product.id
    assert fetched.name == "USB Hub"


def test_get_product_returns_none_for_unknown_product(db_session: Session):
    """get_product returns None when no product matches the given ID."""
    fetched = get_product(db_session, 9999)
    assert fetched is None


def test_update_product_updates_one_field(db_session: Session):
    """update_product updates one field only."""
    product = create_product(db_session, {"name": "Original Name", "price": Decimal("10.00"), "stock": 10})
    updated = update_product(db_session, product.id, {"name": "New Name"})

    assert updated is not None
    assert updated.name == "New Name"
    assert updated.price == Decimal("10.00")
    assert updated.stock == 10


def test_update_product_updates_multiple_fields(db_session: Session):
    """update_product updates multiple fields in one call."""
    product = create_product(db_session, {"name": "Name", "price": Decimal("10.00"), "stock": 10})
    updated = update_product(db_session, product.id, {"name": "New", "price": Decimal("20.00"), "stock": 50})

    assert updated is not None
    assert updated.name == "New"
    assert updated.price == Decimal("20.00")
    assert updated.stock == 50


def test_update_product_empty_dict_preserves_values(db_session: Session):
    """update_product with empty dict preserves existing values."""
    product = create_product(db_session, {"name": "Preserved", "price": Decimal("5.00"), "stock": 8})
    updated = update_product(db_session, product.id, {})

    assert updated is not None
    assert updated.name == "Preserved"
    assert updated.price == Decimal("5.00")
    assert updated.stock == 8


def test_update_product_returns_none_for_unknown_product(db_session: Session):
    """update_product returns None for unknown product ID."""
    result = update_product(db_session, 9999, {"name": "Ghost"})
    assert result is None


def test_delete_product_deletes_and_returns_true(db_session: Session):
    """delete_product deletes an existing product and returns True."""
    product = create_product(db_session, {"name": "Delete Me", "price": Decimal("1.00"), "stock": 1})
    result = delete_product(db_session, product.id)

    assert result is True


def test_delete_product_returns_false_for_unknown_product(db_session: Session):
    """delete_product returns False for unknown product ID."""
    result = delete_product(db_session, 9999)
    assert result is False


def test_deleted_product_not_returned_by_get_product(db_session: Session):
    """After deletion, get_product returns None for the deleted product."""
    product = create_product(db_session, {"name": "Gone", "price": Decimal("3.00"), "stock": 2})
    delete_product(db_session, product.id)

    fetched = get_product(db_session, product.id)
    assert fetched is None


def test_deleting_one_product_does_not_delete_another(db_session: Session):
    """Deleting one product does not affect another product."""
    keep = create_product(db_session, {"name": "Keep", "price": Decimal("7.00"), "stock": 5})
    remove = create_product(db_session, {"name": "Remove", "price": Decimal("2.00"), "stock": 3})

    delete_product(db_session, remove.id)

    still_there = get_product(db_session, keep.id)
    assert still_there is not None
    assert still_there.name == "Keep"

    gone = get_product(db_session, remove.id)
    assert gone is None
