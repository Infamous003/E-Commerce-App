from pydantic import BaseModel
from sqlmodel import SQLModel, Relationship, Field

class Product(SQLModel, table=True):
    __tablename__="products"
    id: str = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    image: str = Field(nullable=False)
    priceCents: int = Field(nullable=False)
    review_stars: float = Field(nullable=False)
    review_count: float = Field(nullable=False)
    
class ProductPublic(BaseModel):
    name: str
    image: str
    priceCents: int
    review_stars: float
    review_count: float

class User(SQLModel, table=True):
    __tablename__ = "user"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(nullable=False, max_length=32, unique=True)
    password: str = Field(nullable=False, max_length=64, min_length=8)
