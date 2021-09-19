from sqlmodel import SQLModel
from sqlmodel import Field
from typing import Optional


class ProductTagLink(SQLModel, table=True):
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )
