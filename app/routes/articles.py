from fastapi import APIRouter, Form, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from app.db import articles_db, users_db
from app.utils.auth import get_current_user
from starlette.status import HTTP_303_SEE_OTHER
from uuid import uuid4

router = APIRouter()

@router.get("/create")
def create_article_page():
    return {"page": "create"}

@router.post("/create")
def create_article(title: str = Form(...), content: str = Form(...), draft: bool = Form(False), request: Request = None, user: str = Depends(get_current_user)):
    article_id = str(uuid4())
    articles_db[article_id] = {
        "id": article_id,
        "title": title,
        "content": content,
        "author": user,
        "is_draft": draft
    }
    users_db[user]["articles"].append(article_id)
    return RedirectResponse(url=f"/article/{article_id}", status_code=HTTP_303_SEE_OTHER)

@router.get("/article/{article_id}")
def get_article(article_id: str, user: str = Depends(get_current_user)):
    article = articles_db.get(article_id)
    if not article or (article["is_draft"] and article["author"] != user):
        raise HTTPException(status_code=404, detail="Статья не найдена")
     return {
        "article": article,
        "similar_articles": similar_articles  
    }
