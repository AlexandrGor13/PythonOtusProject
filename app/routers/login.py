from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.encoders import jsonable_encoder
from app.schemas.user import UserAuth
from app.core.security import create_jwt_token, get_user_from_token
from app.services.user import select_current_user
from app.dependency import auth_user_jwt
from app.core.config import settings

router = APIRouter()

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
        token = create_jwt_token({"login": user_in.login})
        return {"access_token": token, "token_type": "bearer"}
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid credentials"})



@router.get(
    "/about_me"
)
def about_me(
        current_user: Annotated[str, Depends(get_user_from_token)]
):
    """
    Этот маршрут защищен и требует токен. Если токен действителен, мы возвращаем информацию о пользователе.
    """
    if current_user == settings.APP_ADMIN:
        return {'message': 'Access to the protected resource is allowed'}
    user = select_current_user(current_user)
    if user:
        return {'message': 'Access to the protected resource is allowed'}

    return {"error": "User not found"}

