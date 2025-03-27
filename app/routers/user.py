from typing import Annotated

from fastapi import APIRouter, Form, status, Depends, HTTPException, Path, Cookie
from fastapi.params import Cookie
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

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
    select_users,
    select_current_user,
    create_user,
    delete_user,
    update_user,
)

from app.dependency import auth_admin, auth_user

router = APIRouter(
    tags=["Users"],
    prefix="/users"
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
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Server Error"})
    except IntegrityError:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": "User already exists"})
    return JSONResponse(content=jsonable_encoder(user_in))


@router.get(
    "/{username}",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get user",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        }
    },
)
def get_user(
        username: Annotated[str, Path()],
        current_user: Annotated[dict[str], Depends(auth_user)]
):
    try:
        if username == current_user['login'] or current_user['login'] == settings.APP_ADMIN:
            users = select_current_user(username)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except InterfaceError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(users))


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
    # dependencies=[Depends(auth_admin)],
)
def get_users(
        current_user: Annotated[dict[str], Depends(auth_admin)],
        # last_user: Annotated[dict[str], Cookie()]
):
    try:

        users = select_users()
    except InterfaceError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Server Error"})
    response = JSONResponse(content=jsonable_encoder(users))
    response.set_cookie(key='last_user', value=str(current_user))
    return response


@router.put(
    "/{username}",
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
def update_user_param(
        username: Annotated[str, Path()],
        first_name: Annotated[str, Form()],
        last_name: Annotated[str, Form()],
        email: Annotated[EmailStr, Form()],
        phone: Annotated[str, Form()],
        current_user: Annotated[dict[str], Depends(auth_user)]
):
    try:
        if username == current_user['login'] or current_user['login'] == settings.APP_ADMIN:
            user = update_user(
                login=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))


@router.patch(
    "/{username}",
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
        username: Annotated[str, Path()],
        first_name: Annotated[str, Form()],
        last_name: Annotated[str, Form()],
        current_user: Annotated[dict[str], Depends(auth_user)],
):
    try:

        if username == current_user['login'] or current_user['login'] == settings.APP_ADMIN:
            user = update_user(
                login=username,
                first_name=first_name,
                last_name=last_name,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))


@router.patch(
    "/{username}/contacts",
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
        username: Annotated[str, Path()],
        email: Annotated[str, Form()],
        # email: Annotated[EmailStr, Field(description="Электронная почта пользователя")]
        phone: Annotated[str, Form()],
        current_user: Annotated[dict[str], Depends(auth_user)],
):
    try:

        if username == current_user['login'] or current_user['login'] == settings.APP_ADMIN:
            user = update_user(
                login=username,
                email=email,
                phone=phone,
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))


@router.delete(
    "/{username}",
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
def del_user(
        username: Annotated[str, Path()],
        current_user: Annotated[dict[str], Depends(auth_user)]
):
    try:
        if username == current_user['login'] or current_user['login'] == settings.APP_ADMIN:
            user = delete_user(username)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except NoResultFound:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    except InterfaceError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Server Error"})
    return JSONResponse(content=jsonable_encoder(user))
