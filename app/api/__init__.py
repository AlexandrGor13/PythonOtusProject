from .login import router as login_router
from .root import router as root_router
from .users.views import router as users_router
from .dependencies import users_crud

from fastapi import APIRouter

router = APIRouter( )

router.include_router(login_router)
router.include_router(root_router)
router.include_router(users_router)
