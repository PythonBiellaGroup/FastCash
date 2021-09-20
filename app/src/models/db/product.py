from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import String
from sqlalchemy.sql.schema import Column
from sqlmodel import Field, Relationship
from app.src.schemas.entities import ProductBase
from app.src.models.db.link import ProductTagLink

if TYPE_CHECKING:
    from app.src.models.db.product_type import ProductType
    from app.src.models.db.tag import Tag


class Product(ProductBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    
    product_type: Optional["ProductType"] = Relationship(back_populates="products")
    tags: List["Tag"] = Relationship(
        back_populates="products", link_model=ProductTagLink
    )
