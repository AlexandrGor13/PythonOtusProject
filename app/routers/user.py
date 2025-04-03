from typing import Annotated
from fastapi import APIRouter, Form, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.exc import NoResultFound, InterfaceError, IntegrityError

from app.schemas import User as UserSchema, UserRead

from app.services.user import (
    select_current_user,
    create_user,
    delete_user,
    update_user,
)

from app.dependency import get_user_from_token

DEFAULT_STR = ""
DEFAULT_EMAIL = "***@***.***"
DEFAULT_PHONE = "+7**********"

router = APIRouter(tags=["Users"], prefix="/api/users")


@router.post(
    "",
    response_model=UserSchema,
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
def set_user(user_in: Annotated[UserSchema, Form()]):
    try:
        user = create_user(**user_in.__dict__)
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
    return JSONResponse(
        content={
            "description": "User created",
            "user info": jsonable_encoder(user),
        }
    )


@router.get(
    "/me",
    # response_model=UserRead,
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
def about_me(current_user: Annotated[str, Depends(get_user_from_token)]):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    try:
        user = select_current_user(current_user)
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
            "description": "User info",
            "user info": jsonable_encoder(user),
        }
    )


@router.put(
    "/me",
    response_model=UserRead,
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
def update_user_info(
    current_user: Annotated[str, Depends(get_user_from_token)],
    first_name: str = Form(default=DEFAULT_STR),
    last_name: str = Form(default=DEFAULT_STR),
    email: str = Form(default=DEFAULT_EMAIL),
    phone: str = Form(default=DEFAULT_PHONE),
):
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
        user = update_user(**data)
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
            "description": "User updated",
            "user info": jsonable_encoder(user),
        }
    )


@router.delete(
    "/me",
    response_model=UserRead,
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
def del_user(current_user: Annotated[str, Depends(get_user_from_token)]):
    try:
        user = delete_user(current_user)
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
