from typing import Annotated, AnyStr

from fastapi import APIRouter, Form, status, Depends, HTTPException, Path
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
from app.core.security import get_user_from_token
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
    "/me",
    response_model=AnyStr,
    status_code=status.HTTP_200_OK,
    summary="Get user info",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "User not found",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Server Error",
        },
    }
)
def about_me(
        current_user: Annotated[str, Depends(get_user_from_token)]
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    if current_user == settings.APP_ADMIN:
        user = current_user
    else:
        user = select_current_user(current_user)
    if user:
        return JSONResponse(content=jsonable_encoder(user))
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})

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
        if current_user.get('username') == username or current_user.get('username') == settings.APP_ADMIN:
            users = select_current_user(username)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Basic"},
            )
    except Exception:
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
    except Exception:
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
        if current_user.get('username') == username or current_user.get('username') == settings.APP_ADMIN:
            user = update_user(
                username=username,
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

        if current_user.get('username') == username or current_user.get('username') == settings.APP_ADMIN:
            user = update_user(
                username=username,
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

        if current_user.get('username') == username or current_user.get('username') == settings.APP_ADMIN:
            user = update_user(
                username=username,
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
        if current_user.get('username') == username or current_user.get('username') == settings.APP_ADMIN:
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
