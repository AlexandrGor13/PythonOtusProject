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
from .schemas import Profile, ProfileRead, default_profile
from models import Profile as ProfileModel, User as UserModel

from ..get_session import get_async_session


class ProfileCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, profile_in: ProfileRead) -> Profile:
        params = profile_in.model_dump()
        default_params = default_profile.model_dump()
        params = {k: w for k, w in params.items() if default_params[k] != w}
        params["user_id"] = user_id
        profile = ProfileModel(**params)
        self.session.add(profile)
        profile_out = profile.get_schemas
        await self.session.commit()
        return profile_out

    async def update(self, current_user: str, profile_in: ProfileRead) -> Profile:
        params = profile_in.model_dump()
        default_params = default_profile.model_dump()
        params = {k: w for k, w in params.items() if default_params[k] != w}
        user_id = await self.get_id_by_name(current_user)
        statement = (
            update(ProfileModel).where(ProfileModel.user_id == user_id).values(**params)
        )
        await self.session.execute(statement)
        await self.session.commit()
        profile_out = await self.get_by_name(current_user)
        return profile_out

    async def get_by_name(self, username: str) -> Profile:
        statement = select(UserModel).where(UserModel.username == username)
        user = await self.session.scalars(statement)
        user_id = user.one().id
        statement = select(ProfileModel).where(ProfileModel.user_id == user_id)
        profile = await self.session.scalars(statement)
        profile_out = profile.one().get_schemas
        return profile_out

    async def get_id_by_name(self, username: str) -> int:
        statement = select(UserModel).where(UserModel.username == username)
        user = await self.session.scalars(statement)
        user_id = user.one().id
        statement = select(ProfileModel).where(ProfileModel.user_id == user_id)
        profile = await self.session.scalars(statement)
        user_id = profile.one().user_id
        return user_id

    async def get(self) -> list:
        profile_list = []
        statement = select(ProfileModel).order_by(ProfileModel.id)
        profiles = await self.session.scalars(statement)
        for profile in profiles:
            profile_list.append(profile.get_schemas)
        return profile_list


def profile_crud(
    session: Annotated[
        AsyncSession,
        Depends(get_async_session),
    ],
) -> ProfileCRUD:
    return ProfileCRUD(session)
