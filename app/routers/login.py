from typing import Annotated
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, status
from app.schemas.user import UserAuth
from app.core.security import create_jwt_token

from app.dependency import auth_user

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
                    "example": {"access_token": "token", "token_type": "JWT"}
                }
            },
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid credentials",
        },
    },
)
def login(
    # user_agent: Annotated[str, Header()],
    user_in: Annotated[UserAuth, Depends(auth_user)],
):
    """
    Этот маршрут проверяет учетные данные пользователя и возвращает JWT токен, если данные правильные.
    """
    # dev_id = user_agent.get("User-Agent")
    if user_in:
        token = create_jwt_token({"sub": user_in.username})
        return {"access_token": token, "token_type": "JWT"}
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid credentials"},
    )
