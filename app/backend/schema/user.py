
from pydantic import BaseModel, ConfigDict,EmailStr,Field,field_validator
import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)  #i set this 128 why? well for bcrypt can consume lots of cpu cycles. and it follows the OWASP method. 
    confirm_password: str

    @field_validator('confirm_password')
    @classmethod
    def passwords_match(cls, value, info):
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Passwords do not match")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str | None = None
    