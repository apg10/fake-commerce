import pytest
from decimal import Decimal
from pydantic import ValidationError

from backend.app.schemas.product import ProductCreate, ProductRead, ProductUpdate


def test_product_create_accepts_valid_data_and_applies_defaults() -> None:
    product = ProductCreate(name="Shirt", price=Decimal("29.99"))
    assert product.name == "Shirt"
    assert product.description is None
    assert product.stock == 0
    assert product.is_active is True


def test_product_create_rejects_invalid_price() -> None:
    with pytest.raises(ValidationError):
        ProductCreate(name="Bad", price=0)

    with pytest.raises(ValidationError):
        ProductCreate(name="Bad", price=Decimal("-1"))


def test_product_create_rejects_invalid_stock() -> None:
    with pytest.raises(ValidationError):
        ProductCreate(name="Bad", price=Decimal("10"), stock=-1)


def test_product_update_accepts_partial_data() -> None:
    update = ProductUpdate(price="19.99")
    assert update.price == Decimal("19.99")
    assert update.name is None


def test_product_update_rejects_invalid_provided_values() -> None:
    with pytest.raises(ValidationError):
        ProductUpdate(price="0")

    with pytest.raises(ValidationError):
        ProductUpdate(stock=-1)


def test_product_read_supports_orm_style_validation() -> None:
    class DummyObj:
        id = 1
        name = "Laptop"
        description = "A laptop"
        price = Decimal("999.99")
        stock = 5
        is_active = True

    dummy = DummyObj()
    read = ProductRead.model_validate(dummy)
    assert read.id == 1
    assert read.name == "Laptop"
    assert read.description == "A laptop"
    assert read.price == Decimal("999.99")
    assert read.stock == 5
    assert read.is_active is True
