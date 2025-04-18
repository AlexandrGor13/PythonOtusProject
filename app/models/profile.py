from typing import TYPE_CHECKING

from sqlalchemy import (
    String, ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base

if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    __tablename__ = "profiles"

    first_name: Mapped[str] = mapped_column(
        String(50),
        default="",
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
        default="",
    )
    phone: Mapped[str] = mapped_column(
        String(15),
        default="",
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    user: Mapped["User"] = relationship(
        back_populates="profile",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



