
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from db import get_db
from models import Article
from auth import get_current_user
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    articles = db.query(Article).filter(Article.author == user.username).order_by(Article.id.desc()).all()
    return templates.TemplateResponse("profile.html", {
        "request": request,
        "user": user,
        "articles": articles
    })
