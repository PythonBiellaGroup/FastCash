from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List

from app.src.models.link import ProductTagLink

if TYPE_CHECKING:
    from app.src.models.product import Product


class TagBase(SQLModel):
    name: str


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # foreign key = table name
    products: List["Product"] = Relationship(
        back_populates="tags", link_model=ProductTagLink
    )
