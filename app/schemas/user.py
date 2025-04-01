from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated, Optional


class UserRead(BaseModel):
    username: Annotated[str, Field(
        min_length=3,
        max_length=15,
        description="Логин пользователя, от 3 до 15 символов",
    )]
    first_name: Annotated[str, Field(
        max_length=50,
        description="Имя пользователя, от 1 до 50 символов"
    )] = ""
    last_name: Annotated[str, Field(
        max_length=50,
        description="Фамилия пользователя, от 1 до 50 символов"
    )] = ""
    email: Annotated[EmailStr, Field(
        description="Электронная почта пользователя"
    )]
    phone: Annotated[str, Field(
        min_length=5,
        max_length=15,
        description="Номер телефона в международном формате, начинающийся с '+'"
    )]

    # @field_validator('phone')
    # @classmethod
    # def check_valid_phone(cls, phone: str):
    #     if not (phone[1:].isdigit() and phone[0] == '+'):
    #         raise ValueError('Неправильный ввод.')


class User(UserRead):
    password: Annotated[str, Field(
        min_length=8,
        max_length=20,
        description="Пароль пользователя, от 8 до 20 символов"
    )]


class UserAuth(BaseModel):
    username: Annotated[str, Field()]
    password_hash: Annotated[str, Field()]
