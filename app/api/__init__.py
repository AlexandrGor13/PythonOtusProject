from fastapi import APIRouter
from app.api.views.user import router_users

router = APIRouter(
    prefix="/api"
)
router.include_router(router_users)
