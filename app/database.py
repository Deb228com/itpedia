# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Подключение к SQLite (можно заменить на PostgreSQL, если нужно)
SQLALCHEMY_DATABASE_URL = "sqlite:///./itpedia.db"

# Создаём движок базы данных
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создаём сессии для взаимодействия с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Функция для получения сессии (используется в зависимостях)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
