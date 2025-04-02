from fastapi import APIRouter

from .user import router as user_router
from .root import router as root_router
from .login import router as login_router

router = APIRouter(
    prefix="/api/v1",
)
router.include_router(root_router)
router.include_router(login_router)
router.include_router(user_router)

