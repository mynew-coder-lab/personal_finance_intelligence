from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.backend.models.user import User
from app.backend.schema.user import RegisterRequest, LoginRequest, TokenResponse
from app.backend.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

def register_user(db: Session, request: RegisterRequest) -> User:
    """
    Registers a new user by hashing their password and saving them to the database.
    Raises ValueError if the email is already in use.
    """
    # 1. Check if the user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise ValueError("Email already registered")

    # 2. Hash the password
    hashed_pw = hash_password(request.password)

    # 3. Create the database model
    new_user = User(
        email=request.email,
        password_hash=hashed_pw
    )

    # 4. Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def authenticate_user(db: Session, request: LoginRequest) -> TokenResponse:
    """
    Authenticates a user and returns a dual-token pair.
    Raises ValueError on invalid credentials.
    """
    # 1. Fetch user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    # 2. Prevent timing attacks / generic error messages
    if not user or not verify_password(request.password, user.password_hash):
        raise ValueError("Invalid email or password")

    # 3. Update the last login timestamp
    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    # 4. Generate the tokens (Using user_id as the 'sub' subject claim)
    token_data = {"sub": str(user.user_id)}
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # 5. Return the structured Pydantic schema
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )
