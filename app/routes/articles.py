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
