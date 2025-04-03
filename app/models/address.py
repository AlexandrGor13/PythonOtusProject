from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Address(Base):
    __tablename__ = "address"

    address_tip: Mapped[str] = mapped_column(String(50))
    street: Mapped[str] = mapped_column(String(50))
    city: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    country: Mapped[str] = mapped_column(String(50))
    post_index: Mapped[str] = mapped_column(String(10))

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )

    user: Mapped["User"] = relationship(
        back_populates="address",
    )

    def __str__(self):
        return f"{self.post_index}, {self.country}, {self.city}, {self.street}"
