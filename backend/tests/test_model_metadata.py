"""Tests that Product and Category models coexist under the same Base metadata."""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from backend.app.db.base import Base
from backend.app.models.product import Product
from backend.app.models.category import Category


@pytest.fixture()
def test_engine():
    _engine = create_engine("sqlite:///:memory:")
    yield _engine
    _engine.dispose()


@pytest.fixture()
def session(test_engine):
    Base.metadata.create_all(test_engine)
    _session = Session(test_engine)
    yield _session
    _session.close()


class TestProductAndCategoryRegistered:

    def test_product_table_in_metadata(self):
        assert "products" in Base.metadata.tables

    def test_category_table_in_metadata(self):
        assert "categories" in Base.metadata.tables


class TestTableNamesInMetadata:

    def test_metadata_contains_products(self):
        table_names = set(Base.metadata.tables.keys())
        assert "products" in table_names

    def test_metadata_contains_categories(self):
        table_names = set(Base.metadata.tables.keys())
        assert "categories" in table_names


class TestBothTablesCreatedTogether:

    def test_create_both_tables_on_inmemory_engine(self, test_engine):
        Base.metadata.create_all(test_engine)
        inspector = inspect(test_engine)
        tables = set(inspector.get_table_names())
        assert "products" in tables
        assert "categories" in tables


class TestBothInstancesInsertAndQueryIndependently:

    def test_insert_and_query_product_and_category_in_dependent_sessions(self, session: Session):
        product = Product(
            name="Widget",
            description="A useful widget",
            price=99.99,
            stock=50,
        )
        category = Category(name="Widgets", description="All widgets")
        session.add(product)
        session.add(category)
        session.commit()

        fetched_product = session.query(Product).filter_by(name="Widget").one()
        assert fetched_product.name == "Widget"
        assert str(fetched_product.price) == "99.99"

        fetched_category = session.query(Category).filter_by(name="Widgets").one()
        assert fetched_category.name == "Widgets"
