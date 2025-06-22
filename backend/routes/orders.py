from fastapi import APIRouter, HTTPException, status, Depends
from ..models import Order, User, OrderStatus
from ..database import get_session
from sqlmodel import Session, select
from .auth import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def get_orders(session: Session = Depends(get_session)):
    orders = session.exec(
        select(Order)
    ).fetchall()

    return orders

@router.get("/{id}/cancel")
def cancel_order(id: int,
                 session: Session = Depends(get_session),
                 current_user: User = Depends(get_current_user)
                ):
    order_found = session.exec(
        select(Order).where(Order.id == id, Order.customer_id == current_user.id)
    ).one_or_none()

    if order_found is None or order_found.status == OrderStatus.CANCELED:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You do not have an order with ID:{id}")

    order_found.status = OrderStatus.CANCELED
    session.add(order_found)
    session.commit()

    return {"data": f"Order with ID:{id} cancelled"}

@router.get("/{id}/return")
def return_order(id: int,
                 session: Session = Depends(get_session),
                 current_user: User = Depends(get_current_user)
                 ):
    order_found = session.exec(
        select(Order).where(Order.id == id, Order.customer_id == current_user.id)
    ).one_or_none()

    if order_found is None or order_found.status == OrderStatus.RETURNED or order_found.status == OrderStatus.CANCELED:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    
    order_found.status = "RETURNED"
    session.add(order_found)
    session.commit()

    return {"data": f"Order with ID:{order_found.id} returned. You will be refunded within the next 48 hours"}