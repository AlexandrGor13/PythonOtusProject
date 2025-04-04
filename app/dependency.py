from typing import Annotated
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import Depends, status, HTTPException
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
)
from app.core.config import settings
from app.services.user import select_user_password
from app.core.security import verify_password, verify_string
from app.schemas import UserAuth

security_basic = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def auth_admin(credentials: HTTPBasicCredentials = Depends(security_basic)):
    """
    Функция для извлечения информации об администраторе из HTTPBasic авторизации.
    Проверяем логин и пароль администратора.
    """
    is_user_ok = verify_string(credentials.username, settings.APP_ADMIN)
    is_pass_ok = verify_password(credentials.password, settings.APP_PASSWORD)
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": settings.APP_ADMIN, "password": settings.APP_PASSWORD}


def auth_user(credentials: HTTPBasicCredentials = Depends(security_basic)):
    """
    Функция для извлечения информации о пользователе из HTTPBasic авторизации.
    Проверяем логин и пароль пользователя.
    """
    items = list(map(lambda us: UserAuth(**us), select_user_password()))
    for item in items:
        is_user_ok = verify_string(credentials.username, item.username)
        is_pass_ok = verify_password(credentials.password, item.password_hash)
        if is_user_ok and is_pass_ok:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


def auth_user_oath2(credentials: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Функция для извлечения информации о пользователе из OAuth2PasswordBearer авторизации.
    Проверяем логин и пароль пользователя.
    """
    items = list(map(lambda us: UserAuth(**us), select_user_password()))
    for item in items:
        is_user_ok = verify_string(credentials.username, item.username)
        is_pass_ok = verify_password(credentials.password, item.password_hash)
        if is_user_ok and is_pass_ok:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(credentials: Annotated[str, Depends(oauth2_scheme)]):
    """Получение текущего пользователя из токена"""
    try:
        payload = jwt.decode(credentials, settings.SECRET_KEY)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
