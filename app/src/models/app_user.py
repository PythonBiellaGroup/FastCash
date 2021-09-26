from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field

# if TYPE_CHECKING:
#    from app.src.models.db.order import Order


class AppUserBase(SQLModel):
    username: str
    name: Optional[str]
    surname: Optional[str]
    birth_date: Optional[date]
    email: str
    password: str
    isAdmin: bool = False


class AppUser(AppUserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # order: Optional["Order"] = Relationship(back_populates="users")
