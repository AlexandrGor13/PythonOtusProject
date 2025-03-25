from sqlalchemy.orm import Session
from app.core.hashing import pwd_context
from app.schemas.user import UserRead
from app.models import (
    engine,
    User,
    Product,
    Order,
    OrderItem,
    Address,
)


def create_user(login: str, password: str, first_name: str, last_name: str, email: str, phone: str):
    user = User(
        login=login,
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


def select_user():
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
    

def select_user_password():
    with Session(engine) as session:
        try:
            users = session.query(User).all()
            users_list = []
            for user in users:
                users_list.append(user.get_login_password)
        except Exception:
            raise
        finally:
            session.commit()
    return users_list


def update_user(
    login: str,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
) -> UserRead:
    with Session(engine) as session:
        try:
            user_login = session.query(User).filter(User.login == login).one()
            if first_name: user_login.first_name = first_name
            if last_name: user_login.last_name = last_name
            if email: user_login.email = email
            if phone: user_login.phone = phone
            user_out = user_login.get_schemas_user
        except Exception:
            raise
        finally:
            session.commit()
    return user_out


def delete_user(login: str) -> UserRead:
    with Session(engine) as session:
        try:
            user_login = session.query(User).filter(User.login == login).one()
            user_out = user_login.get_schemas_user
            session.delete(user_login)
        except Exception:
            raise
        finally:
            session.commit()
    return user_out
