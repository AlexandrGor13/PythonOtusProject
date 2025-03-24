from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class UserBase(BaseModel):
    login: Annotated[str, Field(
        min_length=3,
        max_length=15,
        description="Логин пользователя, от 3 до 15 символов",
    )]
    email: Annotated[EmailStr, Field(
        description="Электронная почта пользователя"
    )]
    first_name: Annotated[str, Field(
        min_length=1,
        max_length=50,
        description="Имя пользователя, от 1 до 50 символов"
    )] = ""
    last_name: Annotated[str, Field(
        min_length=1,
        max_length=50,
        description="Фамилия пользователя, от 1 до 50 символов"
    )] = ""
    phone: Annotated[str, Field(
        min_length=5,
        max_length=15,
        description="Номер телефона в международном формате, начинающийся с '+'"
    )]


class User(UserBase):
    password: Annotated[str, Field(
        min_length=8,
        max_length=60,
        description="Пароль пользователя, от 8 до 20 символов"
    )]


class UserRead(UserBase):
    id: Annotated[int, Field(
        ge=1,
        description="Идентификатор пользователя"
    )]

class UserUpdate(UserRead, User):
    pass
