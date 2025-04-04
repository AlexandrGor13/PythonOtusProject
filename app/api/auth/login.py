from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.schemas.user import UserAuth
from app.schemas.token import Token
from app.core.security import create_jwt_token

from app.api.auth.dependency import auth_user_oath2

router = APIRouter(tags=["Authentification"])


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User authentification",
    responses={
        status.HTTP_200_OK: {
            "description": "User deleted",
            "content": {
                "application/json": {
                    "example": {"access_token": "token", "token_type": "bearer"}
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
)
def login(
    user_in: Annotated[UserAuth, Depends(auth_user_oath2)],
) -> Token:
    """Функция авторизации пользователя. В случае успеха возвращает токен доступа"""
    token = create_jwt_token({"sub": user_in.username})
    return Token(access_token=token, token_type="bearer")
