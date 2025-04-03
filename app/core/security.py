from datetime import datetime, timedelta, timezone
from jose import jwt
import bcrypt
from passlib.context import CryptContext

from app.core.config import settings

if not hasattr(bcrypt, "__about__"):
    bcrypt.__about__ = type("about", (object,), {"__version__": bcrypt.__version__})

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_jwt_token(data: dict):
    """
    Функция для создания JWT токена.
    Мы копируем входные данные, добавляем время истечения и кодируем токен.
    """
    payload = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expire})
    return jwt.encode(claims=payload, key=settings.SECRET_KEY, algorithm="HS256")
