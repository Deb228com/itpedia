# Это маршруты для редактирования и удаления статьи
from fastapi import APIRouter, Request, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_302_FOUND, HTTP_403_FORBIDDEN

from db import get_db
from models import Article
from auth import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/edit/{article_id}", response_class=HTMLResponse)
def edit_article_form(request: Request, article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article or article.author != user.username:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Нет доступа к статье")

    return templates.TemplateResponse("edit_article.html", {
        "request": request,
        "article": article
    })

@router.post("/edit/{article_id}")
def update_article(article_id: int, title: str = Form(...), content: str = Form(...),
                   db: Session = Depends(get_db), user=Depends(get_current_user)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article or article.author != user.username:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Нет доступа к статье")

    article.title = title
    article.content = content
    db.commit()

    return RedirectResponse(url=f"/article/{article_id}", status_code=HTTP_302_FOUND)

@router.post("/delete/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article or article.author != user.username:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Нет доступа к удалению")

    db.delete(article)
    db.commit()

    return RedirectResponse(url="/", status_code=HTTP_302_FOUND)

