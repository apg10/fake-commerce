import pytest
from pydantic import ValidationError

from backend.app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate


def test_category_create_accepts_valid_data_and_applies_defaults() -> None:
    cat = CategoryCreate(name="Electronics")
    assert cat.name == "Electronics"
    assert cat.description is None
    assert cat.is_active is True


def test_category_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        CategoryCreate(name="")


def test_category_update_accepts_partial_data() -> None:
    update = CategoryUpdate(description="Updated desc")
    assert update.name is None
    assert update.description == "Updated desc"
    assert update.is_active is None


def test_category_update_rejects_empty_name_if_provided() -> None:
    with pytest.raises(ValidationError):
        CategoryUpdate(name="")


def test_category_read_supports_orm_style_validation() -> None:
    class DummyObj:
        id = 1
        name = "Electronics"
        description = "Gadgets and devices"
        is_active = True

    dummy = DummyObj()
    read = CategoryRead.model_validate(dummy)
    assert read.id == 1
    assert read.name == "Electronics"
    assert read.description == "Gadgets and devices"
    assert read.is_active is True
