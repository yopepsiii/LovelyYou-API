from fastapi import FastAPI

from config import settings
from .routers import messages, users, auth

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(messages.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/sqltest")
async def bd_test():
    return {"status": "conection was successful"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


# 6:26:24
