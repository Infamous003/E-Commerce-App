from fastapi import APIRouter, HTTPException, status, Depends
from ..models import Order, User, OrderStatus
from ..database import get_session
from sqlmodel import Session, select
from .auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Shopping cart"])
