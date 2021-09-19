from typing import TYPE_CHECKING, Optional, List
from sqlmodel import Field, Relationship
from app.src.schemas.entities import TagBase
from app.src.models.db.link import ProductTagLink

if TYPE_CHECKING:
    from app.src.models.db.product import Product


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # foreign key = table name
    products: List["Product"] = Relationship(
        back_populates="tags", link_model=ProductTagLink
    )
