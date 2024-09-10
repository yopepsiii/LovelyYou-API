import hashlib
from typing import Callable, Optional

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from .routers import messages, users, auth
from fastapi.middleware.cors import CORSMiddleware

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool
from fastapi_cache import FastAPICache
from fastapi_cache.coder import PickleCoder
from fastapi_cache.backends.redis import RedisBackend

# models.Base.metadata.create_all(bind=engine)

app = FastAPI(root_path='/api/v2')

origins = [
    'http://192.168.31.122:3000',
    'http://localhost:3000'
    'http://localhost:80'
]
app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Какие HTTP-методы разрешены для обработки
    allow_headers=["*"],  # Какие headers разрешены для обработки
)

app.include_router(messages.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "yo doker here132"}


@app.on_event("startup")
async def startup():
    pool = ConnectionPool.from_url(url="redis://redis")
    r = redis.Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(r), prefix="lovely-you-cache", key_builder=api_key_builder)


def api_key_builder(
        func: Callable,
        namespace: Optional[str] = "",
        request: Optional[Request] = None,
        response: Optional[Response] = None,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
) -> str:
    # SOLUTION: https://github.com/long2ice/fastapi-cache/issues/26
    print("kwargs.items():", kwargs.items())
    arguments = {}
    for key, value in kwargs.items():
        if key != 'db':
            arguments[key] = value
    # print("request:", request, "request.base_url:", request.base_url, "request.url:", request.url)
    arguments['url'] = request.url
    # print("arguments:", arguments)

    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    cache_key = (
            prefix
            + hashlib.md5(  # nosec:B303
        f"{func.__module__}:{func.__name__}:{args}:{arguments}".encode()
    ).hexdigest()
    )
    return cache_key
