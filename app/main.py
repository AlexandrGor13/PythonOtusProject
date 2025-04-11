from fastapi import FastAPI

from app.api import router as api_router
from app.internal.admin import create_admin_panel
from app.create_fastapi_app import create_app


app: FastAPI = create_app(
    create_custom_static_urls=True,
)

app.include_router(api_router)
create_admin_panel(app)

