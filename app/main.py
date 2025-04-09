# Это основной файл запуска приложения

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routers import auth, articles, users, search, guide, about
from app.database import create_database
from routes import article  

app.include_router(article.router)


app = FastAPI(
    title="ITPedia",
    description="ITPedia — онлайн-энциклопедия о технологиях",
    version="1.0.0"
)

# CORS (разрешить доступ с любых источников)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Сессии для входа пользователя
app.add_middleware(SessionMiddleware, secret_key="supersecretkey")

# Подключаем маршруты
app.include_router(auth.router)
app.include_router(articles.router)
app.include_router(users.router)
app.include_router(search.router)
app.include_router(guide.router)
app.include_router(about.router)

# Статические файлы (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Создание базы данных при первом запуске
create_database()
