from fastapi import APIRouter, HTTPException, status, Depends
from ..models import Product, ProductPublic, Order, User, Cart
from ..database import get_session
from sqlmodel import Session, select
from .auth import get_current_user
from ..utils import get_product_or_404, get_cart_item_or_404

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[Product], status_code=status.HTTP_200_OK)
def get_products(session: Session = Depends(get_session)):
  products = session.exec(
      select(Product)
  ).fetchall()

  return products

@router.get("/{id}", response_model=ProductPublic, status_code=status.HTTP_200_OK)
def get_product_by_id(id: str, session: Session = Depends(get_session)):

  product = get_product_or_404(id, session)
  return product


@router.get("/{id}/buy")
def buy_product(id: str,
                quantity: int = 1,
                session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)
                ):
  
  product = get_product_or_404(id, session)
  # Here, we are addin a new order to th eorders table
  price = product.priceCents
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
  product = get_product_or_404(id, session)

  cart = session.exec(
     select(Cart).where(Cart.customer_id == current_user.id, Cart.product_id == id)
  ).one_or_none()

  if cart is not None:
     cart.quantity += quantity
     session.add(cart)
     session.commit()
     return {"data": "Added to cart"}

  cart_item = Cart(product_id=id,
                   name=product.name,
                   image=product.image,
                   price_cents=product.priceCents,
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
  
  product = get_product_or_404(id, session)
  cart_item = get_cart_item_or_404(product.id, current_user.id, session)

  if cart_item.quantity > 0 and cart_item.quantity >= quantity:
    cart_item.quantity -= quantity
    session.add(cart_item)

  if cart_item.quantity == 0: session.delete(cart_item)
  session.commit()

  return {"data": "Removed item from the cart"}

