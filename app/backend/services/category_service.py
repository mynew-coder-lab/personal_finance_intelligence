from sqlalchemy.orm import Session
from typing import List
from app.backend.models.category import Category
from app.backend.models.user import User
from app.backend.schema.category import CategoryCreateRequest


def create_category(db: Session, user: User, request: CategoryCreateRequest) -> Category:
    """
    Creates a new income or expense category for the authenticated user.
    Validates parent_category_id if provided (must belong to the user and match type).
    """
    if request.parent_category_id is not None:
        parent = db.query(Category).filter(
            Category.category_id == request.parent_category_id,
            Category.user_id == user.user_id
        ).first()
        if not parent:
            raise ValueError("Parent category not found or does not belong to you")
        if parent.category_type != request.category_type:
            raise ValueError("Parent category type must match child category type")

    category = Category(
        user_id=user.user_id,
        category_name=request.category_name,
        category_type=request.category_type,
        parent_category_id=request.parent_category_id
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_user_categories(db: Session, user: User, category_type: str | None = None) -> List[Category]:
    """
    Retrieves all categories owned by the authenticated user, optionally filtered by type.
    """
    query = db.query(Category).filter(Category.user_id == user.user_id)
    if category_type:
        query = query.filter(Category.category_type == category_type)
    return query.order_by(Category.category_id.asc()).all()


def get_category_by_id(db: Session, user: User, category_id: int) -> Category | None:
    """
    Retrieves a specific category owned by the user.
    """
    return db.query(Category).filter(
        Category.category_id == category_id,
        Category.user_id == user.user_id
    ).first()
