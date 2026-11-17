from sqlalchemy.orm import Session
from typing import List
from app.backend.models.account import Account
from app.backend.models.user import User
from app.backend.schema.account import AccountCreateRequest


def create_account(db: Session, user: User, request: AccountCreateRequest) -> Account:
    """
    Creates a new financial account associated with the authenticated user.
    """
    account = Account(
        user_id=user.user_id,
        account_name=request.account_name,
        account_type=request.account_type,
        currency=request.currency,
        opening_balance=request.opening_balance,
        is_active=True
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


def get_user_accounts(db: Session, user: User) -> List[Account]:
    """
    Retrieves all accounts owned by the authenticated user.
    Guarantees cross-user data isolation.
    """
    return db.query(Account).filter(Account.user_id == user.user_id).order_by(Account.account_id.asc()).all()


def get_account_by_id(db: Session, user: User, account_id: int) -> Account | None:
    """
    Retrieves a specific account only if owned by the authenticated user.
    """
    return db.query(Account).filter(Account.account_id == account_id, Account.user_id == user.user_id).first()
