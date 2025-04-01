import secrets
from typing import Annotated
from fastapi import Form, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm

from app.core.config import settings
from app.services.user import select_user_password
from app.core.security import pwd_context
from app.schemas import UserAuth, User

security = HTTPBasic()


def auth_admin(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, settings.APP_ADMIN)
    is_pass_ok = pwd_context.verify(credentials.password, settings.APP_PASSWORD)
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {'login': settings.APP_ADMIN, 'password': settings.APP_PASSWORD}


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    items = select_user_password()
    items.append({'login': settings.APP_ADMIN, 'password': settings.APP_PASSWORD})
    for item in items:
        is_login_ok = secrets.compare_digest(credentials.username, item.get('login'))
        is_pass_ok = pwd_context.verify(credentials.password, item.get('password'))
        if is_login_ok and is_pass_ok:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

def auth_user_jwt(user_in: Annotated[OAuth2PasswordRequestForm, Depends()],):
    items = list(map(lambda us: UserAuth(**us), select_user_password()))
    items.append(UserAuth(username=settings.APP_ADMIN, password_hash=settings.APP_PASSWORD))
    for item in items:
        is_login_ok = secrets.compare_digest(user_in.username, item.username)
        is_pass_ok = pwd_context.verify(user_in.password, item.password_hash)
        if is_login_ok and is_pass_ok:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "JWT"},
        )

