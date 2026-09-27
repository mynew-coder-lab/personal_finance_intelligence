
from fastapi import APIRouter

from app.backend.schema.user import RegisterRequest, UserResponse, LoginRequest
from app.backend.models.user import User
from app.backend.utils.security import hash_password, verify_password
from app.backend.database.dependencies import get_db


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register_user(request: RegisterRequest):
    return {"message": "User registered successfully.", "user": request}

@router.post("/login", response_model=UserResponse)
def login_user(request: LoginRequest):
    return {"message": "User logged in successfully.", "user": request}