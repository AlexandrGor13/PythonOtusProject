from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class User(BaseModel):
    login: Annotated[str, Field(
        min_length=3,
        max_length=15,
        description="Логин пользователя, от 3 до 15 символов",
    )]
    email: Annotated[EmailStr, Field(
        description="Электронная почта пользователя"
    )]
    first_name: Annotated[str, Field(
        max_length=50,
        description="Имя пользователя, до 50 символов"
    )] = ""
    last_name: Annotated[str, Field(
        max_length=50,
        description="Фамилия пользователя, до 50 символов"
    )] = ""
    phone: Annotated[str, Field(
        max_length=15,
        description="Номер телефона в международном формате, начинающийся с '+'"
    )]


class UserRead(User):
    id: Annotated[int, Field(
        ge=1,
        description="Идентификатор пользователя"
    )]
