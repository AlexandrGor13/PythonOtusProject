from fastapi import FastAPI
from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from fastapi.requests import Request
import uuid
from app.api import router
from app.config import settings
from app.core.security import verify_password, verify_string
from app.models import *


def create_admin_panel(app: FastAPI):
    app.include_router(router)
    admin = Admin(app, async_engine, authentication_backend=authentication_backend)
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(OrderAdmin)
    admin.add_view(OrderItemAdmin)
    admin.add_view(AddressAdmin)


class UserAdmin(ModelView, model=User):
    column_list = [
        column["name"] for column in inspector.get_columns(User.__tablename__)
    ]


class OrderAdmin(ModelView, model=Order):
    column_list = [
        column["name"] for column in inspector.get_columns(Order.__tablename__)
    ]


class AddressAdmin(ModelView, model=Address):
    column_list = [
        column["name"] for column in inspector.get_columns(Address.__tablename__)
    ]


class ProductAdmin(ModelView, model=Product):
    column_list = [
        column["name"] for column in inspector.get_columns(Product.__tablename__)
    ]


class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [
        column["name"] for column in inspector.get_columns(OrderItem.__tablename__)
    ]


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        print(username, settings.admin.user)
        print(password, settings.admin.password)
        is_user_ok = verify_string(username, settings.admin.user)
        is_pass_ok = verify_string(password, settings.admin.password)
        if not (is_user_ok and is_pass_ok):
            return False
        # And update session
        request.session.update({"token": str(uuid.uuid4())})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key=str(uuid.uuid4()))
