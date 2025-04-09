# app/auth.py

from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app import models, database
from sqlalchemy.orm import Session

# Секретный ключ (для безопасности желательно вынести в .env файл)
SECRET_KEY = "super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 дней

# Для шифрования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 схема токена
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Проверка пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Хеширование пароля
def get_password_hash(password):
    return pwd_context.hash(password)

# Создание токена
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Получить текущего пользователя по токену
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Невозможно подтвердить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# Функция получения пользователя через Cookie (для HTML-страниц)
def get_user_from_request(request: Request, db: Session):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return db.query(models.User).filter(models.User.id == int(user_id)).first()
    except JWTError:
        return None

