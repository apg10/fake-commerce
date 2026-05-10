"""Reset in-memory product storage between tests."""

import pytest

from backend.app.routes.products import clear_store


@pytest.fixture(autouse=True)
def _clear_products():
    clear_store()
    yield
