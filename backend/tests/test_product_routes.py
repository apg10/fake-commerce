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


class TestPatchProduct:
    """A-B. PATCH /products/{product_id} updates one or multiple fields."""

    def test_patch_one_field_updates_only_that_field(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "29.99", "stock": 10, "is_active": True},
        )
        product_id = create_resp.json()["id"]
        assert _price_matches(create_resp.json()["price"], 29.99)
        assert create_resp.json()["stock"] == 10
        assert create_resp.json()["is_active"] is True

        response = client.patch(
            f"/products/{product_id}",
            json={"price": "39.99"},
        )
        assert response.status_code == 200
        data = response.json()
        assert _price_matches(data["price"], 39.99)
        assert data["name"] == "Shirt"
        assert data["stock"] == 10
        assert data["is_active"] is True

    def test_patch_multiple_fields_updates_all_provided(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "description": "Old desc", "price": "10.00", "stock": 5, "is_active": False},
        )
        product_id = create_resp.json()["id"]

        response = client.patch(
            f"/products/{product_id}",
            json={
                "name": "Pants",
                "description": "New desc",
                "price": "50.00",
                "stock": 20,
                "is_active": True,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Pants"
        assert data["description"] == "New desc"
        assert _price_matches(data["price"], 50.00)
        assert data["stock"] == 20
        assert data["is_active"] is True


class TestPatchProductNotFound:
    """C. PATCH /products/{product_id} returns 404 for unknown product."""

    def test_patch_unknown_product_returns_404(self):
        response = client.patch(
            "/products/9999",
            json={"name": "Shirt"},
        )
        assert response.status_code == 404


class TestPatchProductValidation:
    """D-G. PATCH /products/{product_id} rejects invalid payloads with 422."""

    def test_patch_price_zero_returns_422(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "10.00"},
        )
        product_id = create_resp.json()["id"]
        response = client.patch(
            f"/products/{product_id}",
            json={"price": 0},
        )
        assert response.status_code == 422

    def test_patch_negative_price_returns_422(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "10.00"},
        )
        product_id = create_resp.json()["id"]
        response = client.patch(
            f"/products/{product_id}",
            json={"price": -5},
        )
        assert response.status_code == 422

    def test_patch_negative_stock_returns_422(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "10.00"},
        )
        product_id = create_resp.json()["id"]
        response = client.patch(
            f"/products/{product_id}",
            json={"stock": -1},
        )
        assert response.status_code == 422

    def test_patch_empty_name_returns_422(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "10.00"},
        )
        product_id = create_resp.json()["id"]
        response = client.patch(
            f"/products/{product_id}",
            json={"name": ""},
        )
        assert response.status_code == 422


class TestDeleteProduct:
    """A. DELETE /products/{product_id} deletes an existing product and returns 204."""

    def test_delete_existing_product_returns_204(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "29.99"},
        )
        product_id = create_resp.json()["id"]
        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 204
        assert response.content == b""

    def test_delete_product_makes_get_return_404(self):
        create_resp = client.post(
            "/products",
            json={"name": "Shirt", "price": "29.99"},
        )
        product_id = create_resp.json()["id"]
        client.delete(f"/products/{product_id}")
        response = client.get(f"/products/{product_id}")
        assert response.status_code == 404

    def test_delete_unknown_product_returns_404(self):
        response = client.delete("/products/9999")
        assert response.status_code == 404

    def test_delete_one_product_does_not_delete_another(self):
        resp_a = client.post(
            "/products",
            json={"name": "Shirt", "price": "29.99"},
        )
        resp_b = client.post(
            "/products",
            json={"name": "Pants", "price": "59.99"},
        )
        id_a = resp_a.json()["id"]
        id_b = resp_b.json()["id"]
        client.delete(f"/products/{id_a}")
        response = client.get(f"/products/{id_b}")
        assert response.status_code == 200
        assert response.json()["name"] == "Pants"


class TestGetProductsFilter:
    """BE-002-A6. GET /products with is_active filter."""

    def test_get_products_no_filter_returns_all(self):
        client.post(
            "/products",
            json={"name": "Active Shirt", "price": "29.99", "is_active": True},
        )
        client.post(
            "/products",
            json={"name": "Inactive Shirt", "price": "19.99", "is_active": False},
        )
        response = client.get("/products")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_get_products_filter_is_active_true(self):
        client.post(
            "/products",
            json={"name": "Active Shirt", "price": "29.99", "is_active": True},
        )
        client.post(
            "/products",
            json={"name": "Inactive Shirt", "price": "19.99", "is_active": False},
        )
        response = client.get("/products?is_active=true")
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["is_active"] is True

    def test_get_products_filter_is_active_false(self):
        client.post(
            "/products",
            json={"name": "Active Shirt", "price": "29.99", "is_active": True},
        )
        client.post(
            "/products",
            json={"name": "Inactive Shirt", "price": "19.99", "is_active": False},
        )
        response = client.get("/products?is_active=false")
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["is_active"] is False

    def test_get_invalid_bool_returns_422(self):
        response = client.get("/products?is_active=maybe")
        assert response.status_code == 422


class TestGetProductsPagination:
    """BE-002-A7. GET /products with limit/offset pagination."""

    def test_get_products_limit_2_returns_2(self):
        for i in range(5):
            client.post(
                "/products",
                json={"name": f"Product{i}", "price": f"{i + 1}.00"},
            )
        response = client.get("/products?limit=2")
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 2

    def test_get_products_offset_1_skips_first(self):
        for i in range(3):
            client.post(
                "/products",
                json={"name": f"Product{i}", "price": f"{i + 1}.00"},
            )
        response = client.get("/products?offset=1")
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]["name"] == "Product1"

    def test_get_products_limit_2_offset_1_returns_expected(self):
        for i in range(5):
            client.post(
                "/products",
                json={"name": f"Product{i}", "price": f"{i + 1}.00"},
            )
        response = client.get("/products?limit=2&offset=1")
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 2
        assert data[0]["name"] == "Product1"
        assert data[1]["name"] == "Product2"

    def test_get_products_limit_0_returns_422(self):
        response = client.get("/products?limit=0")
        assert response.status_code == 422

    def test_get_products_limit_101_returns_422(self):
        response = client.get("/products?limit=101")
        assert response.status_code == 422

    def test_get_products_offset_minus_1_returns_422(self):
        response = client.get("/products?offset=-1")
        assert response.status_code == 422

    def test_get_products_is_active_and_limit_works(self):
        client.post(
            "/products",
            json={"name": "Active1", "price": "10.00", "is_active": True},
        )
        client.post(
            "/products",
            json={"name": "Active2", "price": "20.00", "is_active": True},
        )
        client.post(
            "/products",
            json={"name": "Active3", "price": "30.00", "is_active": True},
        )
        client.post(
            "/products",
            json={"name": "Inactive1", "price": "5.00", "is_active": False},
        )
        response = client.get("/products?is_active=true&limit=1")
        data = response.json()
        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]["is_active"] is True
        assert data[0]["name"] == "Active1"
