from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

from sqlalchemy import (
    MetaData,
    Integer,
    func,
    TIMESTAMP,
    inspect,
    create_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


async_engine = create_async_engine(
    url=settings.db.async_url,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)

engine = create_engine(
    url=settings.db.sync_url,
    echo=settings.db.echo,
    pool_size=settings.db.pool_size,
    max_overflow=settings.db.max_overflow,
)
inspector = inspect(engine)

async_session = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now(), onupdate=func.now()
    )

    # def to_dict(self, exclude_none: bool = False):
    #     """
    #     Преобразует объект модели в словарь.
    #
    #     Args:
    #         exclude_none (bool): Исключать ли None значения из результата
    #
    #     Returns:
    #         dict: Словарь с данными объекта
    #     """
    #     result = {}
    #     for column in inspect(self.__class__).columns:
    #         value = getattr(self, column.key)
    #
    #         # Преобразование специальных типов данных
    #         if isinstance(value, datetime):
    #             value = value.isoformat()
    #         elif isinstance(value, Decimal):
    #             value = float(value)
    #
    #         # Добавляем значение в результат
    #         if not exclude_none or value is not None:
    #             result[column.key] = value
    #
    #     return result
