from fastapi import APIRouter, HTTPException, status, Depends
from ..models import Product, ProductPublic, Order, User, Cart
from ..database import init_db, engine, get_session
from sqlmodel import Session, select
from .auth import get_current_user

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
  
@router.get("/{id}/buy")
def buy_product(id: str,
                quantity: int = 1,
                session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)
                ):
  product_found = session.exec(
    select(Product).where(Product.id == id)
  ).one_or_none()

  if product_found is None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  
  # Here, we are addin a new order to th eorders table
  price = product_found.priceCents
  total_price = quantity * price

  new_order = Order(product_id=id, customer_id=current_user.id, price_cents=price, total_price_cents=total_price)
  session.add(new_order)
  session.commit()
  session.add(new_order)
  
  return {"data": f"Order placed. Track your order with ID:{new_order.id}"}

@router.get("/{id}/add-to-cart")
def add_to_cart(id: str,
                quantity: int = 1,
                session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)
                ):
  product_found = session.exec(
    select(Product).where(Product.id == id)
  ).one_or_none()

  if product_found is None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  cart = session.exec(
     select(Cart).where(Cart.customer_id == current_user.id, Cart.product_id == id)
  ).one_or_none()

  if cart is not None:
     cart.quantity += quantity
     session.add(cart)
     session.commit()
     return {"data": "Added to cart"}

  cart_item = Cart(product_id=id,
                   name=product_found.name,
                   image=product_found.image,
                   price_cents=product_found.priceCents,
                   quantity=quantity,
                   customer_id=current_user.id)
  
  session.add(cart_item)
  session.commit()

  return {"data": "Added to cart"}
  

@router.delete("/{id}/remove-from-cart")
def remove_from_cart(id: str,
                quantity: int = 1,
                session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)
                ):
  
  product_found = session.exec(
    select(Product).where(Product.id == id)
  ).one_or_none()

  if product_found is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
  
  cart_item = session.exec(
    select(Cart).where(Cart.product_id == id)
  ).one_or_none()

  if cart_item is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

  session.delete(cart_item)
  session.commit()

  return {"data": "Removed item from the cart"}

