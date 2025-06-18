from fastapi import Depends
from passlib.context import CryptContext
from .models import User
from sqlmodel import select, Session
from .database import get_session
from datetime import datetime, timedelta, timezone
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "keep this a secret please"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)

def get_user(username: str, session: Session):
    user = session.exec(
        select(User).where(User.username == username)
    ).one_or_none()
    return user

def authenticate_user(username: str, password: str, session: Session = Depends(get_session)):
    user = get_user(username, session)

    if user is None or verify_password(password, user.password) == False:
        return False
    
    return user


def create_access_token(user_data: User, expires_delta: timedelta | None = None):
    to_encode = user_data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
