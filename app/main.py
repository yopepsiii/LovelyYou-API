from fastapi import FastAPI
from .routers import messages, users, auth
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost',
    'http://localhost:8000',
    'https://localhost',
    'https://localhost:8000',
    'https://www.google.com'
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
