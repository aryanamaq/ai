import os
from pathlib import Path
from typing import Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

# Security settings
SECRET_KEY = "your-secret-key-here"  # In production, use a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sample user database - In production, use a real database
USERS_DB = {
    "admin": {
        "username": "admin",
        "hashed_password": pwd_context.hash("password123"),
        "disabled": False
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str):
    if username in USERS_DB:
        return USERS_DB[username]
    return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

class Config:
    UPLOAD_DIR = Path("uploaded_docs")
    ALLOWED_EXTENSIONS = {".docx", ".doc"}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @classmethod
    def init_dirs(cls):
        cls.UPLOAD_DIR.mkdir(exist_ok=True)