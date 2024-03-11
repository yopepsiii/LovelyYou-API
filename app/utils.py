from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    pass


def hash(password: str) -> str:
    return pwd_context.hash(password)
