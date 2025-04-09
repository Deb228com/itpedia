# app/routes.py

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND
from app import models, schemas, utils
from app.database import get_db
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import status
from typing import Optional
from datetime import datetime
from app.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ========== Главная страница ==========

@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    articles = db.query(models.Article).order_by(models.Article.created_at.desc()).all()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles})


# ========== Регистрация ==========

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user_exist = db.query(models.User).filter(models.User.username == username).first()
    if user_exist:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Пользователь уже существует"})
    
    hashed_password = utils.hash_password(password)
    user = models.User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login", status_code=HTTP_302_FOUND)


# ========== Вход ==========

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not utils.verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})

    response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    response.set_cookie("user_id", str(user.id))
    return response


# ========== Выход ==========

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response


# ========== Создание статьи ==========

@router.get("/create", response_class=HTMLResponse)
def create_page(request: Request):
    return templates.TemplateResponse("create_article.html", {"request": request})

@router.post("/create")
def create_article(request: Request, title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    article = models.Article(
        title=title,
        content=content,
        author_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(article)
    db.commit()
    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)


# ========== Просмотр статьи ==========

@router.get("/article/{article_id}", response_class=HTMLResponse)
def view_article(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Статья не найдена")
    return templates.TemplateResponse("article.html", {"request": request, "article": article})


# ========== Создание черновика ==========

@router.get("/drafts", response_class=HTMLResponse)
def drafts_page(request: Request, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    drafts = db.query(models.Draft).filter(models.Draft.author_id == user.id).order_by(models.Draft.updated_at.desc()).all()
    return templates.TemplateResponse("drafts.html", {"request": request, "drafts": drafts})

@router.post("/drafts")
def save_draft(title: str = Form(...), content: str = Form(...), db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    draft = models.Draft(
        title=title,
        content=content,
        author_id=user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(draft)
    db.commit()
    return RedirectResponse(url="/drafts", status_code=HTTP_302_FOUND)


# ========== Гайд ==========

@router.get("/help", response_class=HTMLResponse)
def help_page(request: Request):
    return templates.TemplateResponse("help.html", {"request": request})


# ========== О проекте ==========

@router.get("/about", response_class=HTMLResponse)
def about_page(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


# ========== Поиск ==========

@router.get("/search", response_class=HTMLResponse)
def search(request: Request, q: Optional[str] = None, db: Session = Depends(get_db)):
    results = []
    if q:
        results = db.query(models.Article).filter(models.Article.title.ilike(f"%{q}%") | models.Article.content.ilike(f"%{q}%")).all()
    return templates.TemplateResponse("search.html", {"request": request, "results": results, "query": q})

