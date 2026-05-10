"""Tests for category API routes."""

import pytest
from fastapi.testclient import TestClient

from backend.app.routes.categories import clear_store
from backend.app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_categories():
    clear_store()
    yield


class TestPostCategories:
    """A. POST /categories creates a category with defaults."""

    def test_create_category_returns_201_and_include_id(self):
        response = client.post(
            "/categories",
            json={"name": "Electronics"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert isinstance(data["id"], int)
        assert data["name"] == "Electronics"
        assert data["description"] is None
        assert data["is_active"] is True

    def test_create_category_with_all_fields(self):
        response = client.post(
            "/categories",
            json={
                "name": "Clothing",
                "description": "Shirts and pants",
                "is_active": True,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] is not None
        assert data["name"] == "Clothing"
        assert data["description"] == "Shirts and pants"
        assert data["is_active"] is True

    def test_create_category_with_empty_name_returns_422(self):
        count_before = len(client.get("/categories").json())
        response = client.post(
            "/categories",
            json={"name": ""},
        )
        assert response.status_code == 422
        count_after = len(client.get("/categories").json())
        assert count_before == count_after


class TestGetCategories:
    """B. GET /categories returns created categories."""

    def test_list_categories_returns_created_categories(self):
        client.post(
            "/categories",
            json={"name": "Electronics"},
        )
        client.post(
            "/categories",
            json={"name": "Clothing"},
        )
        response = client.get("/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["name"] == "Electronics"
        assert data[1]["name"] == "Clothing"


class TestGetCategoryById:
    """C. GET /categories/{category_id} returns an existing category."""

    def test_get_existing_category(self):
        create_resp = client.post(
            "/categories",
            json={"name": "Electronics"},
        )
        category_id = create_resp.json()["id"]
        response = client.get(f"/categories/{category_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == "Electronics"

    """D. GET /categories/{category_id} returns 404 for unknown category."""

    def test_get_404_for_unknown_category(self):
        response = client.get("/categories/9999")
        assert response.status_code == 404
