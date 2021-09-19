from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship
from app.src.schemas.entities import ProductTypeBase


if TYPE_CHECKING:
    from app.src.models.db.product import Product


class ProductType(ProductTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] = Relationship(back_populates="product_type")
