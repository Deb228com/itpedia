# Это маршрут отображения отдельной статьи
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from db import get_db
from models import Article
from auth import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/article/{article_id}", response_class=HTMLResponse)
def read_article(request: Request, article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Статья не найдена")

    return templates.TemplateResponse("article.html", {
        "request": request,
        "article": article,
        "user": user
    })
@router.post("/create")

async def create_post(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    form = await request.form()
    title = form.get("title")
    content = form.get("content")
    category = form.get("category")
    tags = form.get("tags")

    article = Article(
        title=title,
        content=content,
        author=user.username,
        category=category,
        tags=tags
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    return RedirectResponse(url=f"/article/{article.id}", status_code=302)
@router.get("/article/{id}", response_class=HTMLResponse)
def read_article(id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == id).first()
    if not article:
        return RedirectResponse(url="/", status_code=302)

    # Находим похожие статьи по категории или тегам
    similar_articles = db.query(Article).filter(
        Article.id != id,
        (
            (Article.category == article.category) |
            (Article.tags != None and article.tags != None and Article.tags.op('LIKE')(f"%{article.tags.split(',')[0].strip()}%"))
        )
    ).limit(5).all()

    return templates.TemplateResponse("article.html", {
        "request": request,
        "article": article,
        "similar_articles": similar_articles
    })
