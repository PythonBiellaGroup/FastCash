from typing import Optional
from app.src.schemas.entities import ProductBase


class ProductRead(ProductBase):
    id: int
    name: str
    description: str
    price: float
    available: bool


class ProductCreate(ProductBase):
    name: str
    description: str
    price: float
    available: bool


class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None


class ProductDelete(ProductBase):
    pass
