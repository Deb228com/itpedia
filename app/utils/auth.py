# app/utils/auth.py

from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Хэшируем пароль
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Проверяем пароль
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Генерация уникального ID сессии
def create_session() -> str:
    return str(uuid.uuid4())
