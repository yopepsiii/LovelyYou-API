from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from .routers import messages, users

from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(messages.router)
app.include_router(users.router)

templates = Jinja2Templates(directory="templates")

@app.get("/sqltest")
async def bd_test():
    return {"status": "conection was successful"}


@app.get("/")
async def root():
    return {"message": "Hello World"}





# 6:26:24
