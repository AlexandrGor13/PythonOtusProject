from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import UsersCRUD
from app.models.base import async_session


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session


def users_crud(
    session: Annotated[
        AsyncSession,
        Depends(get_async_session),
    ],
) -> UsersCRUD:
    return UsersCRUD(session)


# async def get_users(
#     current_user: Annotated[str, Depends(get_current_user)],
#     crud: Annotated[UsersCRUD, Depends(users_crud)],
# ):
#     try:
#         user = crud.get_by_name(current_user)
#         if user:
#             users = await crud.get()
#             users_out = [user.get_schemas_user for user in users]
#     except NoResultFound:
#         return JSONResponse(
#             status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
#         )
#     except InterfaceError:
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={"detail": "Server Error"},
#         )
#     return JSONResponse(
#         content={jsonable_encoder(users_out)}
#     )
