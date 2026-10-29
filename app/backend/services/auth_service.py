from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.backend.models.user import User
from app.backend.schema.user import RegisterRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from app.backend.utils.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

def register_user(db: Session, request: RegisterRequest) -> User:
    """
    Registers a new user by hashing their password and saving them to the database.
    Raises ValueError if the email is already in use.
    """
    # 1. Check if the user already exists
    existing_user = db.query(User).filter(User.email == request.email).first() #select * from users where email = value_from_request.email limit 1;
    if existing_user:
        raise ValueError("Email already registered")

    # 2. Hash the password
    hashed_pw = hash_password(request.password) #this is for security, like for encryption but not exact.

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
    user = db.query(User).filter(User.email == request.email).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise ValueError("Invalid email or password")

    user.last_login_at = datetime.now(timezone.utc)
    db.commit()

    token_data = {"sub": str(user.user_id)}
    
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

def refresh_access_token(db: Session, request: RefreshTokenRequest) -> TokenResponse:
    payload = decode_token(request.refresh_token)
    if not payload:
        raise ValueError("Invalid refresh token")
    
    elif payload.get("type") != "refresh":
        raise ValueError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise ValueError("token invalid")
    
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise ValueError("User not found")

    new_access_token = create_access_token({"sub": str(user.user_id)})


    return TokenResponse(
        access_token=new_access_token,
        refresh_token=request.refresh_token,
        token_type="bearer"
    )
