import secrets
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import (
    Form,
    Depends,
    status,
    HTTPException
)
from fastapi.security import (
    HTTPBasic,
    HTTPBearer,
    HTTPBasicCredentials,
    HTTPAuthorizationCredentials,
)
from app.core.config import settings
from app.services.user import select_user_password
from app.core.security import pwd_context
from app.schemas import UserAuth, User

security_basic = HTTPBasic()
security_bearer = HTTPBearer()


def auth_admin(credentials: HTTPBasicCredentials = Depends(security_basic)):
    is_user_ok = secrets.compare_digest(credentials.username, settings.APP_ADMIN)
    is_pass_ok = pwd_context.verify(credentials.password, settings.APP_PASSWORD)
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {'username': settings.APP_ADMIN, 'password': settings.APP_PASSWORD}


def auth_user(credentials: HTTPBasicCredentials = Depends(security_basic)):
    items = list(map(lambda us: UserAuth(**us), select_user_password()))
    for item in items:
        is_user_ok = secrets.compare_digest(credentials.username, item.username)
        is_pass_ok = pwd_context.verify(credentials.password, item.password_hash)
        if is_user_ok and is_pass_ok:
            return item
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )


def get_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(security_bearer)):
    """
    Функция для извлечения информации о пользователе из токена. Проверяем токен и извлекаем утверждение о пользователе.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        username = payload.get('sub')
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to validate credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return username
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
