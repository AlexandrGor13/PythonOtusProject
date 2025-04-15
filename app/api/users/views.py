from typing import Annotated
from fastapi import APIRouter, Body, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.exc import NoResultFound, InterfaceError, IntegrityError


from schemas import User as UserSchema
from .crud import UsersCRUD
from .dependencies import users_crud

from ..auth.dependencies import get_current_user

DEFAULT_STR = ""
DEFAULT_EMAIL = "***@***.***"
DEFAULT_PHONE = "+7**********"

router = APIRouter(tags=["Users"], prefix="/users")


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    summary="Create user",
    responses={
        status.HTTP_200_OK: {
            "description": "User created",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User created",
                        "user info": {
                            "username": "string",
                            "first_name": "",
                            "last_name": "",
                            "email": "user@example.com",
                            "phone": "string",
                            "password": "stringst",
                        },
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {"description": "User already exists"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def set_user(
    user_in: Annotated[UserSchema, Body()],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Создание нового пользователя
    """
    try:
        user = await crud.create(user_in)
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    except IntegrityError:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "User already exists"},
        )
    return {
            "description": "User created",
            "user info": user,
        }


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get user info",
    responses={
        status.HTTP_200_OK: {
            "description": "User info",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User info",
                        "user info": {
                            "username": "string",
                            "first_name": "",
                            "last_name": "",
                            "email": "user@example.com",
                            "phone": "string",
                            "password": "stringst",
                        },
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def about_me(
        current_user: Annotated[str, Depends(get_current_user)],
        crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    try:
        user = await crud.get_by_name(current_user)
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return {
            "description": "User info",
            "user info": user,
        }


@router.get(
    "/all_users",
    status_code=status.HTTP_200_OK,
)
async def all_users(
        crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    try:
        users = await crud.get()
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return users


@router.put(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Update user",
    responses={
        status.HTTP_200_OK: {
            "description": "User updated",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User updated",
                        "user info": {
                            "username": "string",
                            "first_name": "",
                            "last_name": "",
                            "email": "user@example.com",
                            "phone": "string",
                            "password": "stringst",
                        },
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def update_user_info(
    current_user: Annotated[str, Depends(get_current_user)],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
    first_name: str = Body(default=DEFAULT_STR),
    last_name: str = Body(default=DEFAULT_STR),
    email: str = Body(default=DEFAULT_EMAIL),
    phone: str = Body(default=DEFAULT_PHONE),
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы можем изменить информацию о пользователе.
    """
    try:
        data = {"username": current_user}
        if first_name != DEFAULT_STR:
            data["first_name"] = first_name
        if last_name != DEFAULT_STR:
            data["last_name"] = last_name
        if email != DEFAULT_EMAIL:
            data["email"] = email
        if phone != DEFAULT_PHONE:
            data["phone"] = phone
        user = await crud.update(**data)
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return {
            "description": "User updated",
            "user info": user,
        }



@router.delete(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    responses={
        status.HTTP_200_OK: {
            "description": "User deleted",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User deleted",
                        "user info": {
                            "username": "string",
                            "first_name": "",
                            "last_name": "",
                            "email": "user@example.com",
                            "phone": "string",
                            "password": "stringst",
                        },
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
async def del_user(
    current_user: Annotated[str, Depends(get_current_user)],
    crud: Annotated[UsersCRUD, Depends(users_crud)],
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы можем удалить пользователя.
    """
    try:
        user = await crud.delete(current_user)
    except NoResultFound:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"}
        )
    except InterfaceError:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Server Error"},
        )
    return JSONResponse(
        content={
            "detail": "User deleted",
            "user info": jsonable_encoder(user),
        }
    )
