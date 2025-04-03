from typing import TYPE_CHECKING, List

from sqlalchemy import (
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from app.schemas.user import UserRead

if TYPE_CHECKING:
    from .order import Order
    from .address import Address


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(15),
        unique=True
    )    
    password_hash: Mapped[str | None] = mapped_column(
        String(256),
        default=None,
    )
    first_name: Mapped[str] = mapped_column(
        String(50),
        default="",
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
        default="",
    )
    email: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )
    phone: Mapped[str] = mapped_column(
        String(15),
        default="",
    )
    order: Mapped[List["Order"]] = relationship(
        back_populates="owner",
    )
    address: Mapped["Address"] = relationship(
        back_populates="user",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def get_schemas_user(self) -> UserRead:
        return UserRead(
            username=self.username,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
        )
        
    @property
    def get_username_password(self) -> dict:
        return {'username': self.username, 'password_hash': self.password_hash}
