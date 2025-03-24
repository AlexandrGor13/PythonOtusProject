from app.api.crud.hash_pw import hash_password
from sqlalchemy.orm import Session
from app.models import (
    engine,
    User,
    Product,
    Order,
    OrderItem,
    Address,
)


def create_user(login, password, first_name, last_name, email, phone):
    user = User(
        login=login,
        password_hash=hash_password(password),
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone
    )
    with Session(engine) as session:
        try:
            session.add(user)
            session.flush()
            user_out = user.get_schemas_user
        except Exception:
            raise
        finally:
            session.commit()
    return user_out


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


def select_user_and_password():
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


def update_user(id, login, password, first_name, last_name, email, phone):
    with Session(engine) as session:
        try:
            user_id = session.query(User).filter(User.id == id).one()
            user_id.login = login
            user_id.password_hash = hash_password(password)
            user_id.first_name = first_name
            user_id.last_name = last_name
            user_id.email = email
            user_id.phone = phone
            user_out = user_id.get_schemas_user
        except Exception:
            raise
        finally:
            session.commit()
    return user_out


def delete_user(id: int):
    with Session(engine) as session:
        try:
            user_id = session.query(User).filter(User.id == id).one()
            user_out = user_id.get_schemas_user
            session.delete(user_id)
        except Exception:
            raise
        finally:
            session.commit()
    return user_out
