from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas.user import UserAuth
from app.core.security import create_jwt_token, get_user_from_token

from app.dependency import auth_user_jwt
from app.core.config import settings

router = APIRouter(
    tags=['Authentication']
)

@router.post(
    "/login",
    # response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="User authentication",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        }
    },
)
def login(
        user_in: Annotated[UserAuth, Depends(auth_user_jwt)]
):
    """
    Этот маршрут проверяет учетные данные пользователя и возвращает JWT токен, если данные правильные.
    """

    if user_in:
        token = create_jwt_token({"username": user_in.username})
        return {"access_token": token, "token_type": "bearer"}
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials"})





