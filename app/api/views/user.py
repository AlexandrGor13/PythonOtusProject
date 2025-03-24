from fastapi import APIRouter, Form, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.exc import (
    NoResultFound,
    InterfaceError,
    IntegrityError
)

from app.schemas import (
    User as UserSchema,
    UserRead
)
from typing import Annotated

from app.api.crud.user import (
    select_user,
    create_user,
    delete_user,
    update_user,
)

from app.api.dependencies import authenticate

router_users = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router_users.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Insert user",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "User already exists"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    },
)
def set_user(user_in: Annotated[UserSchema, Form()]):
    try:
        create_user(**user_in.__dict__)
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    except IntegrityError:
        return JSONResponse(status_code=409, content={"detail": "User already exists"})
    return JSONResponse(content=jsonable_encoder(user_in))


@router_users.get(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Get users",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        }
    },
    dependencies=[Depends(authenticate)]
)
def get_user():
    try:
        users = select_user()
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(users))


@router_users.put(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Update user",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        }
    },
)
def put_user(user_in: Annotated[UserRead, Form()]):
    try:
        user = update_user(**user_in.model_dump())
    except NoResultFound:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))


@router_users.delete(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Delete user",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        }
    },
)
def del_user(id: Annotated[int, Form()]):
    try:
        user = delete_user(id)
    except NoResultFound:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))
