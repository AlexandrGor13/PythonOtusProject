import os


class Settings:
    PROJECT_NAME = "OtusProject"
    PROJECT_VERSION = "0.1.0"

    APP_ADMIN = os.getenv("APP_ADMIN")
    APP_PASSWORD = os.getenv("APP_PASSWORD")
    SECRET_KEY = os.getenv("SECRET_KEY")
    TOKEN_URL = "/login"

    PG_DB = os.getenv("PG_DB")
    PG_USER = os.getenv("PG_USER")
    PG_PASSWORD = os.getenv("PG_PASSWORD")
    PG_HOST = os.getenv("PG_HOST")
    PG_PORT = os.getenv("PG_PORT")


    SQLA_PG_ENGINE = "asyncpg"
    SQLA_PG_URL = f"postgresql+{SQLA_PG_ENGINE}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    SQLA_ECHO = True
    SQLA_POOL_SIZE = 50
    SQLA_MAX_OVERFLOW = 0
    SQLA_NAMING_CONVENTION = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


settings = Settings()
