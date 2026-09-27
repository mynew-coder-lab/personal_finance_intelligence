import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
#.encode("utf-8") converts to bytes    
#bcrypt.gensalt() adds random salt
# bcrypt.hashpw(...) does the cryptographic hash
# .decode("utf-8") converts back to a clean string for PostgreSQL

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

#why i used bcrypt is because it intentionally slows down the number of trials the hackers try to decode
#this protects against brute force attacks

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(
        timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
#this line i used mainly for the creation and epiration of teh token and that will done using pyjwt. mainly it is mapped with the timeline correctly and based on that i have given the access token and refresh token to the user.

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(
        timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
#this line is used to create refresh token and it is also mapped with the timeline correctly and based on that i have given the access token and refresh token to the user.


def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
#this line is used to decode the access token and refresh token.