from fastapi import FastAPI

import uvicorn

from app.api import router
from app.internal.admin import create_admin

app = FastAPI()

app.include_router(router)
create_admin(app)

if __name__ == "__main__":
    from dotenv import load_dotenv
    import pathlib

    path_env = pathlib.Path(__file__).parents[-1] / ".env"
    load_dotenv(path_env)

    uvicorn.run("main:app", reload=True)
