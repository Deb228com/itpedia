# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routes import articles, users, auth, general
from app import models
from app.database import engine

# Создание всех таблиц в базе данных
models.Base.metadata.create_all(bind=engine)

# Инициализация FastAPI приложения
app = FastAPI(title="ITPedia")

# Подключение статических файлов (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Шаблонизатор Jinja2
templates = Jinja2Templates(directory="app/templates")

# Настройка CORS (если понадобится фронт на другом домене)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов
app.include_router(general.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(articles.router)

# Главная точка входа
@app.get("/")
def root():
    return {"message": "Добро пожаловать на ITPedia"}
