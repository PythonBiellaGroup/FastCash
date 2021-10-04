from typing import Optional
from sqlalchemy.sql.schema import Column
from sqlalchemy import String
from sqlmodel import SQLModel, Field


class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    available: bool


# Classe per interagire con il db
class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))


# Classi di validazione pydantic per API
class ProductRead(ProductBase):
    id: int


class ProductCreate(ProductBase):
    available: Optional[bool] = True


class ProductUpdate(ProductBase):
    name: str = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
