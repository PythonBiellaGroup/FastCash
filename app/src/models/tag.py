from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import String
from sqlalchemy.sql.schema import Column
from typing import TYPE_CHECKING, Optional, List

from app.src.models.link import ProductTagLink

if TYPE_CHECKING:
    from app.src.models.product import Product


class TagBase(SQLModel):
    name: str


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    # foreign key = table name
    products: List["Product"] = Relationship(
        back_populates="tags", link_model=ProductTagLink
    )


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int


# Nel modello update tutti gli attributi devono essere opzionali
class TagUpdate(SQLModel):
    name: Optional[str] = None
