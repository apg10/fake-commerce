"""Tests for the product repository using an in-memory SQLite database."""

from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.models.product import Product
from backend.app.repositories.product_repository import create_product, get_product, list_products


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
