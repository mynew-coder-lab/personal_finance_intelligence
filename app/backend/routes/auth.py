
from app.backend.schema.user import TokenResponse
from app.backend.services import auth_service
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from app.backend.schema.user import RegisterRequest, UserResponse, LoginRequest, RefreshTokenRequest
from app.backend.database.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model = UserResponse)
def register_user(request: RegisterRequest, db: Session = Depends(get_db)):
    try:
        new_user = auth_service.register_user(db, request)
        return new_user

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        token = auth_service.authenticate_user(db, request)
        return token
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.post("/refresh", status_code=status.HTTP_200_OK, response_model=TokenResponse)
def refresh(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    try:
        new_token = auth_service.refresh_access_token(db, request)
        return new_token
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


