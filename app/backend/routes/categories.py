from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.backend.database.dependencies import get_db, get_current_user
from app.backend.models.user import User
from app.backend.schema.category import CategoryCreateRequest, CategoryResponse
from app.backend.services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def create_category_endpoint(
    request: CategoryCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        new_category = category_service.create_category(db, current_user, request)
        return new_category
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
def get_categories_endpoint(
    category_type: Optional[str] = Query(None, pattern="^(income|expense)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = category_service.get_user_categories(db, current_user, category_type=category_type)
    return categories
