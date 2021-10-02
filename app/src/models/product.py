from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String
from sqlalchemy.sql.schema import Column
from app.src.models.link import ProductTagLink
from app.src.models.product_type import ProductTypeRead
from app.src.models.product_type import ProductType
from app.src.models.tag import Tag, TagRead


class ProductBase(SQLModel):
    name: str
    description: str
    price: float
    available: bool
    type_id: Optional[int] = Field(default=None, foreign_key="producttype.id")


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    product_type: Optional[ProductType] = Relationship(back_populates="products")
    tags: List[Tag] = Relationship(
        back_populates="products", link_model=ProductTagLink
    )


class ProductRead(ProductBase):
    id: int
    name: str
    description: str
    price: float
    available: bool
    # type_id: Optional[int] = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None
    type_id: Optional[int] = None


class ProductReadwithTypeAndTags(ProductRead):
    product_type: Optional[ProductTypeRead] = None
    tags: List[TagRead] = []
