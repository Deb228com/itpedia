# 📁 app/routes/profile.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.utils.auth import auth_required
from app.models import Article
from app.utils.users import get_current_user
from app.templates import templates

router = APIRouter()

@router.get("/profile", response_class=HTMLResponse)
@auth_required
async def profile_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request)
    articles = db.query(Article).filter(Article.author_id == user.id).all()
    drafts = db.query(Article).filter(Article.author_id == user.id, Article.is_draft == True).all()

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "articles": articles,
        "drafts": drafts
    })
