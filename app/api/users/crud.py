"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas.user import UserRead, User as UserSchema
from app.core.security import get_password_hash
from app.models import (
    engine,
    User,
    Product,
    Order,
    OrderItem,
    Address,
)


class UsersCRUD:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_in: UserSchema) -> UserRead:
        params = user_in.model_dump()
        params['password_hash'] = params.pop('password')
        user = User(**params)
        self.session.add(user)
        user_out = user.get_schemas_user
        self.session.commit()
        return user_out

    def update_user(self, user_in: UserRead) -> UserRead:
        user = self.session.query(User).filter(User.username == user_in.username).one()
        if user.first_name:
            user.first_name = user_in.first_name
        if user.last_name:
            user.last_name = user_in.last_name
        if user.email:
            user.email = user_in.email
        if user.phone:
            user.phone = user_in.phone
        user_out = user.get_schemas_user
        self.session.commit()
        return user_out

    def delete_user(self, username: str) -> UserRead:
        user = self.session.query(User).filter(User.username == username).one()
        self.session.delete(user)
        user_out = user.get_schemas_user
        self.session.commit()
        return user_out

    def get_current_user(self, username: str) -> UserRead:
        user = self.session.query(User).filter(User.username == username).one()
        user_out = user.get_schemas_user
        return user_out

    def get_user_password(self) -> list:
        users_list = []
        users = self.session.query(User).all()
        for user in users:
            users_list.append(user.get_username_password)
        return users_list