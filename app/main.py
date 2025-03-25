from fastapi import FastAPI

import uvicorn

from app.routers import router

app = FastAPI()
app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
