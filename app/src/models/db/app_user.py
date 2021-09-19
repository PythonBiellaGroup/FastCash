from typing import TYPE_CHECKING, Optional
from sqlmodel import Field, Relationship
from app.src.schemas.entities import AppUserBase

if TYPE_CHECKING:
    from app.src.models.db.order import Order


class AppUser(AppUserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    order: Optional["Order"] = Relationship(back_populates="users")
