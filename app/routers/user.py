from typing import Annotated

from fastapi import APIRouter, Form, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.exc import (
    NoResultFound,
    InterfaceError,
    IntegrityError
)

from app.core.config import settings
from app.schemas import (
    User as UserSchema,
    UserRead
)

from app.services.user import (
    select_user,
    create_user,
    delete_user,
    update_user,
)

from app.dependency import auth_admin, auth_user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.post(
    "",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    summary="Create user",
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


@router.get(
    "",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get users",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        }
    },
    dependencies=[Depends(auth_admin)],
)
def get_user():
    try:
        users = select_user()
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(users))


@router.put(
    "",
    response_model=UserRead,
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
def update_user_param(user_in: Annotated[UserRead, Form()], current_user: Annotated[str, Depends(auth_user)]):
    try:
        if user_in.login == current_user or current_user == settings.APP_LOGIN:
            user = update_user(**user_in.model_dump())
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))


@router.patch(
    "",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update name user",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        }
    },
)
def update_name_user(
        login: Annotated[str, Form()],
        first_name: Annotated[str, Form()],
        last_name: Annotated[str, Form()],
        current_user: Annotated[str, Depends(auth_user)],
):
    try:

        if login == current_user or current_user == settings.APP_LOGIN:
            user = update_user(login, **{'first_name': first_name, 'last_name': last_name})
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))


@router.patch(
    "/contacts",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Update contact user",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        }
    },
)
def update_contact_user(
        login: Annotated[str, Form()],
        email: Annotated[str, Form()],
        # email: Annotated[EmailStr, Field(description="Электронная почта пользователя")]
        phone: Annotated[str, Form()],
        current_user: Annotated[str, Depends(auth_user)],
):
    try:

        if login == current_user or current_user == settings.APP_LOGIN:
            user = update_user(login, **{'email': email, 'phone': phone})
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))


@router.delete(
    "",
    response_model=UserRead,
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
def del_user(login: Annotated[str, Form()], current_user: Annotated[str, Depends(auth_user)]):
    try:
        if login == current_user or current_user == settings.APP_LOGIN:
            user = delete_user(login)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=404, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=500, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))
