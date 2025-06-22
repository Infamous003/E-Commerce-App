from fastapi import APIRouter, HTTPException, status, Depends
from ..models import Order
from ..database import init_db, engine, get_session
from sqlmodel import Session, select

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/")
def get_orders(session: Session = Depends(get_session)):
    orders = session.exec(
        select(Order)
    )

    return orders