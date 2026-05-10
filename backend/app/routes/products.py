"""Products API routes with in-memory storage."""

from fastapi import APIRouter, HTTPException, Query

from backend.app.schemas import ProductCreate, ProductRead, ProductUpdate

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


@router.patch("/products/{product_id}", response_model=ProductRead)
def patch_product(product_id: int, product_update: ProductUpdate) -> ProductRead:

    product = _products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = product_update.model_dump(exclude_unset=True)
    updated_product = {**product.model_dump(), **update_data}
    final_product = ProductRead(**updated_product)
    _products[product_id] = final_product
    return final_product


@router.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int) -> None:
    product = _products.pop(product_id, None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")


@router.get("/products", response_model=list[ProductRead])
def list_products(
    is_active: bool | None = Query(default=None),
    limit: int = Query(default=100, gt=0, le=100),
    offset: int = Query(default=0, ge=0),
) -> list[ProductRead]:
    products = list(_products.values())
    if is_active is not None:
        products = [p for p in products if p.is_active == is_active]
    return products[offset : offset + limit]


@router.get("/products/{product_id}", response_model=ProductRead)
def get_product(product_id: int) -> ProductRead:
    product = _products.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
