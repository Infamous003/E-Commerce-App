from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from .models import User, Product, Cart, Order
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

# Utility functions related to products

def get_product_or_404(id: str, session: Session = Depends(get_session)):
  product = session.exec(
      select(Product).where(Product.id == id)
  ).one_or_none()

  if product is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  return product


def get_cart_item_or_404(id: str,
                  user_id: int,
                  session: Session = Depends(get_session)):
  cart_item = session.exec(
      select(Cart).where(Cart.product_id == id, Cart.customer_id == user_id)
  ).one_or_none()

  if cart_item is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  
  return cart_item


def get_order_or_404(id: int,
                     user_id: int,
                     session: Session = Depends(get_session),
                     error_msg = "Order not found"):
  order = session.exec(
    select(Order).where(Order.id == id, Order.customer_id == user_id)
  ).one_or_none()

  if order is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_msg)
  return order
