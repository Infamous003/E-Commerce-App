from fastapi import APIRouter, HTTPException, status, Depends
from ..models import Order, User, OrderStatus, Cart
from ..database import get_session
from sqlmodel import Session, select
from .auth import get_current_user

router = APIRouter(prefix="/cart", tags=["Shopping cart"])

@router.get("/")
def get_my_cart_items(session: Session = Depends(get_session),
                      current_user: User = Depends(get_current_user)):
    cart_items = session.exec(
        select(Cart).where(Cart.customer_id == current_user.id)
    ).fetchall()

    return cart_items
