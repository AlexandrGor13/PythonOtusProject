from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    Numeric,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .order_items import OrderItem


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    image_url: Mapped[str] = mapped_column(String(150))
    order: Mapped["OrderItem"] = relationship(
        back_populates="item",
    )

    def __str__(self):
        return self.name
