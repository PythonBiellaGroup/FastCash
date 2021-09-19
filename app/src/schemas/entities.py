from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class AppUserBase(SQLModel):
    name: str
    email: str
    password: str
    isAdmin: bool = False


class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    available: bool
    type_id: Optional[int] = Field(default=None, foreign_key="producttype.id")


class ProductTypeBase(SQLModel):
    name: str


class TagBase(SQLModel):
    name: str


class MenuBase(SQLModel):
    name: str
    description: str
    price: str
    available: bool = True


class OrderBase(SQLModel):
    total_price: float
    discount: float
    order_time: datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note: str
