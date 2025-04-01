from sqlalchemy.orm import Session
from app.core.security import pwd_context
from app.schemas.user import UserRead
from app.models import (
    engine,
    User,
    Product,
    Order,
    OrderItem,
    Address,
)


def create_user(username: str, password: str, first_name: str, last_name: str, email: str, phone: str):
    user = User(
        username=username,
        password_hash=pwd_context.hash(password),
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone
    )
    with Session(engine) as session:
        try:
            session.add(user)
        except Exception:
            raise
        finally:
            session.commit()
    return user


def select_users():
    with Session(engine) as session:
        try:
            users = session.query(User).all()
            users_list = []
            for user in users:
                users_list.append(user.get_schemas_user)
        except Exception:
            raise
        finally:
            session.commit()
    return users_list


def select_current_user(username: str):
    with Session(engine) as session:
        try:
            user = session.query(User).filter(User.username == username).one()
            user_out = user.get_schemas_user
        except Exception:
            raise
        finally:
            session.commit()
    return user_out


def select_user_password():
    with Session(engine) as session:
        try:
            users = session.query(User).all()
            users_list = []
            for user in users:
                users_list.append(user.get_username_password)
        except Exception:
            raise
        finally:
            session.commit()
    print(users_list)
    return users_list


def update_user(
        username: str,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
) -> UserRead:
    with Session(engine) as session:
        try:
            user = session.query(User).filter(User.username == username).one()
            if first_name: user.first_name = first_name
            if last_name: user.last_name = last_name
            if email: user.email = email
            if phone: user.phone = phone
            user_out = user.get_schemas_user
        except Exception:
            raise
        finally:
            session.commit()
    return user_out


def delete_user(username: str) -> UserRead:
    with Session(engine) as session:
        try:
            user = session.query(User).filter(User.username == username).one()
            user_out = user.get_schemas_user
            session.delete(user)
        except Exception:
            raise
        finally:
            session.commit()
    return user_out


