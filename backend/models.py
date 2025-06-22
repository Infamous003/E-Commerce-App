from pydantic import BaseModel
from sqlmodel import SQLModel, Relationship, Field
from datetime import datetime
from enum import Enum

class Product(SQLModel, table=True):
    __tablename__="products"
    id: str = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    image: str = Field(nullable=False)
    priceCents: int = Field(nullable=False)
    review_stars: float = Field(nullable=False)
    review_count: float = Field(nullable=False)

    order: list["Order"] = Relationship(back_populates="product")
    
class ProductPublic(BaseModel):
    name: str
    image: str
    priceCents: int
    review_stars: float
    review_count: float

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, max_length=32, unique=True)
    password: str = Field(nullable=False, max_length=64, min_length=8)

    order: list["Order"] = Relationship(back_populates="user")

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class OrderStatus(str, Enum):
    DELIVERED = "Delivered"
    ARRIVING = "Arriving"
    CANCELED = "Canceled"
    RETURNED = "Returned"

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    id: int | None = Field(default=None, primary_key=True)
    product_id: str = Field(foreign_key="products.id", ondelete="CASCADE")
    price_cents: int = Field()
    quantity: int = Field(default=1)
    total_price_cents: int = Field()
    customer_id: int = Field(foreign_key="users.id", ondelete="CASCADE")
    date_of_order: datetime = Field(default_factory=datetime.now)
    status: OrderStatus = Field(default=OrderStatus.ARRIVING)
    
    # address
    # total price
    
    product: Product = Relationship(back_populates="order")
    user: User = Relationship(back_populates="order")
