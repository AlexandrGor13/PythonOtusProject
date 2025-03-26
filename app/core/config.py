import os
from dotenv import load_dotenv
from pathlib import Path, PurePath

env_path = PurePath(Path.cwd()).parents[1]/'.env'

load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME = 'OtusProject'
    PROJECT_VERSION = '1.0.0'

    APP_ADMIN = "admin"
    APP_PASSWORD = "$2b$12$ykSu89iSKPepZj8rMAd4..5.eRTq.YXDu2azfy/.6nzE50YdTpK9a"

    PG_DB = "app_database"
    PG_USER = "app"
    PG_PASSWORD = "password"
    PG_HOST = "localhost"
    PG_PORT = 5432

    SQLA_PG_ENGINE = "pg8000"
    SQLA_PG_URL = f"postgresql+{SQLA_PG_ENGINE}://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    SQLA_ECHO = True
    SQLA_NAMING_CONVENTION = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


settings = Settings()


if __name__ == '__main__':
    print(env_path)
    print(PurePath(Path.cwd()).parents[1] / '.env')
    print(os.getenv("APP_ADMIN"))
