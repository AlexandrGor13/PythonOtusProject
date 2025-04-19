"""
Create
Read
Update
Delete
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import get_password_hash
from .schemas import UserRead, User as UserSchema, default_user
from models import User as UserModel

from ..get_session import get_async_session


class UsersCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_in: UserSchema) -> UserRead:
        params = user_in.model_dump()
        params["password_hash"] = get_password_hash(params.pop("password"))
        user = UserModel(**params)
        self.session.add(user)
        user_out = user.get_schemas
        await self.session.commit()
        return user_out

    async def update(self, current_user: str, user_in: UserSchema) -> UserRead:
        params = user_in.model_dump()
        default_params = default_user.model_dump()
        params = {k: w for k, w in params.items() if default_params[k] != w}
        if params.get("password"):
            params["password_hash"] = get_password_hash(params.pop("password"))
        statement = (
            update(UserModel).where(UserModel.username == current_user).values(**params)
        )
        await self.session.execute(statement)
        await self.session.commit()
        username_new = params.get("username")
        current_user = username_new if username_new else current_user
        user_out = await self.get_by_name(current_user)
        return user_out

    async def delete(self, current_user: str) -> UserRead:
        statement = delete(UserModel).where(UserModel.username == current_user)
        user_out = await self.get_by_name(current_user)
        await self.session.execute(statement)
        await self.session.commit()
        return user_out

    async def get_by_name(self, username: str) -> UserRead:
        statement = select(UserModel).where(UserModel.username == username)
        user = await self.session.scalars(statement)
        user_out = user.one().get_schemas
        return user_out

    async def get_id_by_name(self, username: str) -> int:
        statement = select(UserModel).where(UserModel.username == username)
        user = await self.session.scalars(statement)
        user_id = user.one().id
        return user_id

    async def get_users_and_password(self) -> list:
        users_list = []
        statement = select(UserModel).order_by(UserModel.id)
        users = await self.session.scalars(statement)
        for user in users.all():
            users_list.append(user.get_username_password)
        return users_list

    async def get(self) -> list:
        users_list = []
        statement = select(UserModel).order_by(UserModel.id)
        users = await self.session.scalars(statement)
        for user in users:
            users_list.append(user.get_schemas)
        return users_list


def users_crud(
    session: Annotated[
        AsyncSession,
        Depends(get_async_session),
    ],
) -> UsersCRUD:
    return UsersCRUD(session)
