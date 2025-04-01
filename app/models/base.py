from datetime import datetime
from decimal import Decimal
from app.core.config import settings

from sqlalchemy import (
    create_engine,
    MetaData,
    Integer,
    func,
    TIMESTAMP,
    inspect,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,

)

engine = create_engine(
    settings.SQLA_PG_URL,
    echo=settings.SQLA_ECHO,
)

inspector = inspect(engine)


class Base(DeclarativeBase):
    metadata = MetaData(
        naming_convention=settings.SQLA_NAMING_CONVENTION,
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )

    def to_dict(self, exclude_none: bool = False):
        """
        Преобразует объект модели в словарь.

        Args:
            exclude_none (bool): Исключать ли None значения из результата

        Returns:
            dict: Словарь с данными объекта
        """
        result = {}
        for column in inspect(self.__class__).columns:
            value = getattr(self, column.key)

            # Преобразование специальных типов данных
            if isinstance(value, datetime):
                value = value.isoformat()
            elif isinstance(value, Decimal):
                value = float(value)

            # Добавляем значение в результат
            if not exclude_none or value is not None:
                result[column.key] = value

        return result

