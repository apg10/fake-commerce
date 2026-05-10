"""Products API routes with in-memory storage."""

from fastapi import APIRouter, HTTPException

from backend.app.schemas import ProductCreate, ProductRead

router = APIRouter(tags=["products"])

_products: dict[int, ProductRead] = {}
_next_id: int = 1


def clear_store():
    """Clear in-memory store (used by tests)."""
    _products.clear()
    global _next_id
    _next_id = 1


@router.post("/products", response_model=ProductRead, status_code=201)
def create_product(product: ProductCreate) -> ProductRead:
    global _next_id
    read = ProductRead(
        id=_next_id,
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        is_active=product.is_active,
    )
    _products[_next_id] = read
    _next_id += 1
    return read


@router.get("/products", response_model=list[ProductRead])
def list_products() -> list[ProductRead]:
    return list(_products.values())


@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int) -> ProductRead:
    product = _products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
