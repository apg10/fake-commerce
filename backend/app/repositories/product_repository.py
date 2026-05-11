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
