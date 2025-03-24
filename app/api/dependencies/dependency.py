import secrets

from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import settings

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, settings.APP_LOGIN)
    is_pass_ok = secrets.compare_digest(credentials.password, settings.APP_PASSWORD)
    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
