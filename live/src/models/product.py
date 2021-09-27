from typing import Optional
from sqlalchemy.sql.schema import Column
from sqlalchemy import String
from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    available: bool


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
