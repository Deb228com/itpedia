# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Адрес подключения к SQLite (можно сменить на PostgreSQL при необходимости)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./itpedia.db")

# Создаём движок SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Создаём сессию подключения к БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей (мы его используем в models.py как Base)
Base = declarative_base()
