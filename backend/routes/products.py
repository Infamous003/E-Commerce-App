from fastapi import APIRouter, HTTPException, status, Depends
from ..models import Product, ProductPublic
from ..database import init_db, engine, get_session
from sqlmodel import Session, select

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[ProductPublic], status_code=status.HTTP_200_OK)
def get_products(session: Session = Depends(get_session)):
  products = session.exec(
      select(Product)
  ).fetchall()

  return products

@router.get("/{id}", response_model=ProductPublic, status_code=status.HTTP_200_OK)
def get_product_by_id(id: str, session: Session = Depends(get_session)):
  product_found = session.exec(
    select(Product).where(Product.id == id)
  ).one_or_none()
  
  if product_found is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  else:
      return product_found