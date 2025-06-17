from pydantic import BaseModel
from sqlmodel import SQLModel, Relationship, Field

class Rating(BaseModel):
    stars: float
    count: int

# class Product(SQLModel, table=True):
#     __tablename__="products"
#     id: str | None = None
#     name: str
#     image: str
#     priceCents: int
#     review_stars: float

class Product(SQLModel, table=True):
    __tablename__="products"
    id: str = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    image: str = Field(nullable=False)
    priceCents: int = Field(nullable=False)
    review_stars: float = Field(nullable=False)
    review_count: float = Field(nullable=False)
    