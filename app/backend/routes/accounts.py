from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.backend.database.dependencies import get_db, get_current_user
from app.backend.models.user import User
from app.backend.schema.account import AccountCreateRequest, AccountResponse
from app.backend.services import account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AccountResponse)
def create_account_endpoint(
    request: AccountCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        new_account = account_service.create_account(db, current_user, request)
        return new_account
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", status_code=status.HTTP_200_OK, response_model=List[AccountResponse])
def get_accounts_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    accounts = account_service.get_user_accounts(db, current_user)
    return accounts
