from pydantic import BaseModel

class Rating(BaseModel):
    stars: float
    count: int

class Product(BaseModel):
    id: str | None = None
    name: str
    image: str
    priceCents: int
    rating: Rating
    keywords: list[str]
    