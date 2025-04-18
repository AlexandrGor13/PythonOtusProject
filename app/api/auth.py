from typing import Annotated
from fastapi import APIRouter, Depends, status, Body, HTTPException

from .users.schemas import UserAuth
from .token import Token
from core.security import create_jwt_token
from .dependencies import auth_user_oath2, oauth2_scheme

router = APIRouter(tags=["Authentification"])
blacklist = set()

@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="User authentification",
    responses={
        status.HTTP_200_OK: {
            "description": "User login",
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

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    summary="User authentification",
    responses={
        status.HTTP_200_OK: {
            "description": "User logout",
            "content": {
                "application/json": {
                    "example": {"access_token": "token", "token_type": "bearer"}
                }
            },
        },
    },
)
def logout(token: Annotated[Token, Body()]):
    blacklist.add(token.access_token)
    return {"msg": "Successfully logged out"}





@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    if token in blacklist:
        raise HTTPException(status_code=403, detail="Token has been blacklisted")
    return {"msg": "Access granted"}