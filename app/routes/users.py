from fastapi import APIRouter, Depends, HTTPException
from app.db import users_db, articles_db
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/profile")
def get_profile(user: str = Depends(get_current_user)):
    user_data = users_db.get(user)
    if not user_data:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    authored_articles = [articles_db[aid] for aid in user_data["articles"] if aid in articles_db]
    return {"username": user, "articles": authored_articles}

