from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderItem(Base):
    __tablename__ = "order_items"

    order_id: Mapped[int] = mapped_column(
        ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
    )
    item: Mapped["Product"] = relationship(
        back_populates="order",
    )
    order: Mapped["Order"] = relationship(
        back_populates="order_item",
    )

    def __str__(self):
        return self.name
