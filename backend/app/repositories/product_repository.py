"""Product repository with SQLAlchemy session."""

from sqlalchemy.orm import Session

from backend.app.models.product import Product


def create_product(db: Session, data: dict) -> Product:
    """Create a new product and persist it."""
    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session) -> list[Product]:
    """Return all products."""
    return db.query(Product).all()


def get_product(db: Session, product_id: int) -> Product | None:
    """Return a product by ID or None if not found."""
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(db: Session, product_id: int, data: dict) -> Product | None:
    """Update an existing product with fields from data dict. Returns None if not found."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return None
    for key, value in data.items():
        if hasattr(product, key):
            setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    """Delete a product by ID. Returns True if deleted, False if not found."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        return False
    db.delete(product)
    db.commit()
    return True
