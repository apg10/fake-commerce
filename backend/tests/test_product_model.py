"""Tests for SQLAlchemy Product model."""

from decimal import Decimal

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.models.product import Product


@pytest.fixture()
def test_engine():
    _engine = create_engine("sqlite:///:memory:")
    yield _engine
    _engine.dispose()


@pytest.fixture()
def session(test_engine: "Engine"):
    Base.metadata.create_all(test_engine)
    _session = Session(test_engine)
    yield _session
    _session.close()


class TestProductTableName:

    def test_table_name_is_products(self):
        assert Product.__tablename__ == "products"


class TestProductColumns:

    def test_id_column_exists_and_is_correct_type(self):
        mapper = Product.__mapper__
        columns = {c.key: c.type for c in mapper.columns}
        assert "id" in columns
        assert columns["id"].python_type == int

    def test_name_column_exists_and_is_required_string(self):
        mapper = Product.__mapper__
        columns = {c.key: c for c in mapper.columns}
        assert "name" in columns
        assert "name" in columns
        assert columns["name"].nullable is False

    def test_description_column_allows_none(self):
        mapper = Product.__mapper__
        columns = {c.key: c for c in mapper.columns}
        assert "description" in columns
        assert columns["description"].nullable is True

    def test_price_column_exists(self):
        mapper = Product.__mapper__
        columns = {c.key: c.type for c in mapper.columns}
        assert "price" in columns

    def test_stock_column_exists_and_default_is_zero(self):
        mapper = Product.__mapper__
        columns = {c.key: c for c in mapper.columns}
        assert "stock" in columns
        p = Product(name="Shirt", price=Decimal("10.00"))
        assert p.stock == 0

    def test_is_active_column_exists_and_default_is_true(self):
        p = Product(name="Shirt", price=Decimal("10.00"))
        assert p.is_active is True


class TestProductTableCreation:

    def test_metadata_creates_tables(self, test_engine):
        Base.metadata.create_all(test_engine)
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "products" in tables


class TestProductPersistAndQuery:

    def test_create_and_query_product(self, session: Session):
        product = Product(
            name="Shirt",
            description="A cotton shirt",
            price=Decimal("29.99"),
            stock=10,
            is_active=True,
        )
        session.add(product)
        session.commit()
        session.refresh(product)
        assert product.id is not None
        fetched = session.query(Product).filter_by(id=product.id).one()
        assert fetched.name == "Shirt"

    def test_filter_by_is_active(self, session: Session):
        s1 = Product(name="Active1", price=Decimal("10.00"))
        s2 = Product(name="Inactive1", price=Decimal("5.00"), is_active=False)
        session.add_all([s1, s2])
        session.commit()
        active = session.query(Product).filter_by(is_active=True).all()
        assert len(active) == 1
        assert active[0].name == "Active1"


class TestProductDefaults:

    def test_stock_default_is_zero(self):
        p = Product(name="Shirt", price=Decimal("10.00"))
        assert p.stock == 0

    def test_is_active_default_is_true(self):
        p = Product(name="Shirt", price=Decimal("10.00"))
        assert p.is_active is True

    def test_stock_default_can_be_overridden(self):
        p = Product(name="Shirt", price=Decimal("10.00"), stock=25)
        assert p.stock == 25

    def test_is_active_default_can_be_overridden(self):
        p = Product(name="Shirt", price=Decimal("10.00"), is_active=False)
        assert p.is_active is False
