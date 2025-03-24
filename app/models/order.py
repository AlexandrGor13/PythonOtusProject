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

from .db import Base

if TYPE_CHECKING:
    from .user import User
    from .order_items import OrderItem


class Order(Base):
    __tablename__ = "orders"

    name: Mapped[str] = mapped_column(String(50))
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    owner: Mapped["User"] = relationship(
        back_populates="order",
    )
    order_item: Mapped["OrderItem"] = relationship(
        back_populates="order",
    )

    def __str__(self):
        return self.name