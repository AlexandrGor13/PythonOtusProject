"""
Create
Read
Update
Delete
"""

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserRead, User as UserSchema
from app.core.security import get_password_hash
from app.models import (
    async_engine,
    User,
    Product,
    Order,
    OrderItem,
    Address,
)


class UsersCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_in: UserSchema) -> UserRead:
        params = user_in.model_dump()
        params['password_hash'] = params.pop('password')
        user = User(**params)
        self.session.add(user)
        user_out = user.get_schemas_user
        await self.session.commit()
        return user_out

    async def update(self,
        username: str,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
    ) -> UserRead:

        values = []
        if first_name: values.append({"first_name": first_name})
        if last_name: values.append({"last_name": last_name})
        if email: values.append({"email": email})
        if phone: values.append({"phone": phone})
        statement = update(User).where(User.username == username).values(*values)
        await self.session.execute(statement)
        user_out = await self.get_by_name(username)
        await self.session.commit()
        return user_out

    async def delete(self, username: str) -> UserRead:
        statement = delete(User).where(User.username == username)
        await self.session.execute(statement)
        user_out = await self.get_by_name(username)
        await self.session.commit()
        return user_out

    async def get_by_name(self, username: str) -> UserRead:
        statement = select(User).where(User.username == username)
        user = await self.session.scalars(statement)
        user_out = user.one().get_schemas_user
        return user_out

    async def get_users_and_password(self) -> list:
        users_list = []
        statement = select(User).order_by(User.id)
        users = await self.session.scalars(statement)
        for user in users.all():
            users_list.append(user.get_username_password)
        return users_list

    async def get(self) -> list:
        users_list = []
        statement = select(User).order_by(User.id)
        users = await self.session.scalars(statement)
        for user in users:
            users_list.append(user.get_schemas_user)
        return users_list