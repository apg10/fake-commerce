"""Categories API routes with in-memory storage."""

from fastapi import APIRouter, HTTPException

from backend.app.schemas.category import CategoryCreate, CategoryRead

router = APIRouter(tags=["categories"])

_categories: dict[int, CategoryRead] = {}
_next_id: int = 1


def clear_store():
    """Clear in-memory store (used by tests)."""
    _categories.clear()
    global _next_id
    _next_id = 1


@router.post("/categories", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate) -> CategoryRead:
    global _next_id
    read = CategoryRead(
        id=_next_id,
        name=category.name,
        description=category.description,
        is_active=category.is_active,
    )
    _categories[_next_id] = read
    _next_id += 1
    return read


@router.get("/categories", response_model=list[CategoryRead])
def list_categories() -> list[CategoryRead]:
    return list(_categories.values())


@router.get("/categories/{category_id}", response_model=CategoryRead)
def get_category(category_id: int) -> CategoryRead:
    category = _categories.get(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
