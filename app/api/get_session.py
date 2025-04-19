from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from models.base import async_session


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session