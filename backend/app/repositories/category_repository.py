"""Category repository with SQLAlchemy session."""

from sqlalchemy.orm import Session

from backend.app.models.category import Category


def create_category(db: Session, data: dict) -> Category:
    """Create a new category and persist it."""
    category = Category(**data)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def list_categories(db: Session) -> list[Category]:
    """Return all categories."""
    return db.query(Category).all()


def get_category(db: Session, category_id: int) -> Category | None:
    """Return a category by ID or None if not found."""
    return db.query(Category).filter(Category.id == category_id).first()
