import secrets
from app.api.crud.hash_pw import hash_password
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.config import settings
from app.api.crud.user import select_user_and_password

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, settings.APP_LOGIN)
    is_pass_ok = secrets.compare_digest(credentials.password, settings.APP_PASSWORD)
    if not (is_user_ok and is_pass_ok):
        users = select_user_and_password()
        print(len(users))
        for user in users:
            print(user["login"], user["password"])

            # if not (secrets.compare_digest(user["login"], credentials.username) and
            #         secrets.compare_digest(user["password"], hash_password(credentials.password))):
            #     raise HTTPException(
            #         status_code=status.HTTP_401_UNAUTHORIZED,
            #         detail="Invalid credentials",
            #         headers={"WWW-Authenticate": "Basic"},
            #     )
