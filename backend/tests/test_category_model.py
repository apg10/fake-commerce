"""Tests for SQLAlchemy Category model."""

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from backend.app.db.base import Base
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


class TestCategoryTableName:

    def test_table_name_is_categories(self):
        assert Category.__tablename__ == "categories"


class TestCategoryColumns:

    def test_id_column_exists_and_is_correct_type(self):
        mapper = Category.__mapper__
        columns = {c.key: c.type for c in mapper.columns}
        assert "id" in columns
        assert columns["id"].python_type == int

    def test_name_column_exists_and_is_required_string(self):
        mapper = Category.__mapper__
        columns = {c.key: c for c in mapper.columns}
        assert "name" in columns
        assert columns["name"].nullable is False

    def test_description_column_allows_none(self):
        mapper = Category.__mapper__
        columns = {c.key: c for c in mapper.columns}
        assert "description" in columns
        assert columns["description"].nullable is True

    def test_is_active_column_exists_and_is_boolean(self):
        mapper = Category.__mapper__
        columns = {c.key: c.type for c in mapper.columns}
        assert "is_active" in columns


class TestCategoryTableCreation:

    def test_metadata_creates_categories_table(self, test_engine):
        Base.metadata.create_all(test_engine)
        inspector = inspect(test_engine)
        tables = inspector.get_table_names()
        assert "categories" in tables


class TestCategoryPersistAndQuery:

    def test_create_and_query_category(self, session: Session):
        category = Category(
            name="Electronics",
            description="Electronic devices and accessories",
            is_active=True,
        )
        session.add(category)
        session.commit()
        session.refresh(category)
        assert category.id is not None
        fetched = session.query(Category).filter_by(id=category.id).one()
        assert fetched.name == "Electronics"

    def test_filter_by_is_active(self, session: Session):
        c1 = Category(name="ActiveCat")
        c2 = Category(name="InactiveCat", is_active=False)
        session.add_all([c1, c2])
        session.commit()
        active = session.query(Category).filter_by(is_active=True).all()
        assert len(active) == 1
        assert active[0].name == "ActiveCat"


class TestCategoryDefaults:

    def test_is_active_default_is_true(self):
        c = Category(name="DefaultCat")
        assert c.is_active is True

    def test_is_active_default_can_be_overridden(self):
        c = Category(name="OverridenCat", is_active=False)
        assert c.is_active is False
