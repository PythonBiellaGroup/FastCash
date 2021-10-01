from sqlmodel import SQLModel
from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship

if TYPE_CHECKING:
    from app.src.models.product import ProductRead
    from app.src.models.product import Product


class ProductTypeBase(SQLModel):
    name: str
    description: str


class ProductType(ProductTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    description: Optional[str] = Field(default=None)
    products: List["Product"] = Relationship(back_populates="product_type")


# class ProductTypeRead(ProductTypeBase):
#     id: int
#     name: str
#     description: str
#     # products: List["Product"]


class ProductTypeReadwithProduct(ProductTypeBase):
    product_type: Optional["ProductRead"] = None


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeRead(ProductTypeBase):
    id: int


# Nel modello update tutti gli attributi devono essere opzionali
class ProductTypeUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None

