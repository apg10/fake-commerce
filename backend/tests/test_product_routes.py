"""Tests for product API routes."""

import pytest
from decimal import Decimal
from fastapi.testclient import TestClient

from backend.app.routes.products import clear_store
from backend.app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_products():
    clear_store()
    yield


def _price_matches(actual, expected):
    """Compare price values allowing Decimal and float/string representation from FastAPI/JSON."""
    return Decimal(str(actual)) == Decimal(str(expected))


class TestPostProducts:
    """A. POST /products creates a product."""

    def test_create_product_returns_201_and_include_id(self):
        response = client.post(
            "/products",
            json={"name": "Shirt", "price": "29.99"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert isinstance(data["id"], int)
        assert data["name"] == "Shirt"
        assert _price_matches(data["price"], 29.99)
        assert data["description"] is None
        assert data["stock"] == 0
        assert data["is_active"] is True

    def test_create_product_with_all_fields(self):
        response = client.post(
            "/products",
            json={
                "name": "Laptop",
                "description": "A powerful laptop",
                "price": "999.99",
                "stock": 5,
                "is_active": True,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Laptop"
        assert data["description"] == "A powerful laptop"
        assert _price_matches(data["price"], 999.99)
        assert data["stock"] == 5
        assert data["is_active"] is True


class TestGetProducts:
    """B. GET /products returns created products."""

    def test_list_products_returns_created_products(self):
        client.post(
            "/products",
            json={"name": "Shirt", "price": "29.99"},
        )
        response = client.get("/products")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["name"] == "Shirt"
        assert _price_matches(data[0]["price"], 29.99)


class TestGetProductById:
    """C. GET /products/{product_id} returns an existing product."""

    def test_get_existing_product(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "29.99"},
        )
        product_id = create_resp.json()["id"]
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Shirt"

    def test_get_404_for_unknown_product(self):
        response = client.get("/products/9999")
        assert response.status_code == 404


class TestInvalidProductCreation:
    """Invalid product payloads return 422 and do not pollute the store."""

    def test_create_product_with_price_zero_returns_422(self):
        count_before = len(client.get("/products").json())
        response = client.post(
            "/products",
            json={"name": "Shirt", "price": 0},
        )
        assert response.status_code == 422
        count_after = len(client.get("/products").json())
        assert count_before == count_after

    def test_create_product_with_negative_price_returns_422(self):
        count_before = len(client.get("/products").json())
        response = client.post(
            "/products",
            json={"name": "Shirt", "price": -5},
        )
        assert response.status_code == 422
        count_after = len(client.get("/products").json())
        assert count_before == count_after

    def test_create_product_with_negative_stock_returns_422(self):
        count_before = len(client.get("/products").json())
        response = client.post(
            "/products",
            json={"name": "Shirt", "price": 10, "stock": -1},
        )
        assert response.status_code == 422
        count_after = len(client.get("/products").json())
        assert count_before == count_after

    def test_create_product_missing_name_returns_422(self):
        count_before = len(client.get("/products").json())
        response = client.post(
            "/products",
            json={"price": 10},
        )
        assert response.status_code == 422
        count_after = len(client.get("/products").json())
        assert count_before == count_after
