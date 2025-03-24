from fastapi import FastAPI

import uvicorn

from app.api import router as api_router

app = FastAPI()
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
