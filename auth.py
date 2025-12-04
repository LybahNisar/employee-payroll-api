# auth.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# ------------------ Password Hashing ----------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash password with bcrypt (truncate to 72 chars to avoid bcrypt limit)
    """
    truncated_password = password[:72]
    return pwd_context.hash(truncated_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify hashed password (truncate to 72 chars for bcrypt limit)
    """
    truncated_password = plain_password[:72]
    return pwd_context.verify(truncated_password, hashed_password)


# ------------------ JWT Settings ------------------
SECRET_KEY = "your_secret_key_here"  # Replace with a secure secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour


# ------------------ JWT Token ------------------
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """
    Decode JWT token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# ------------------ JWT Bearer ------------------
class JWTBearer(HTTPBearer):
    """
    Custom JWT Auth class to allow token only in header
    Usage: Depends(JWTBearer())
    """
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            token = credentials.credentials  # Accept token directly without "Bearer "
            payload = decode_access_token(token)
            if payload is None:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token or expired")
            return payload
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid authorization")
