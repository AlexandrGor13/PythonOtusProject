import secrets

from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.core.config import settings
from app.services.user import select_user_password
from app.core.hashing import pwd_context

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
        is_login_ok = secrets.compare_digest(credentials.username, item['login'])
        is_pass_ok = pwd_context.verify(credentials.password, item['password'])
        if is_login_ok and is_pass_ok:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
