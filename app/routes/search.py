from fastapi import APIRouter, Query
from app.db import articles_db

router = APIRouter()

@router.get("/search")
def search_articles(q: str = Query("")):
    results = []
    for article in articles_db.values():
        if q.lower() in article["title"].lower() or q.lower() in article["content"].lower():
            if not article["is_draft"]:
                results.append(article)
    return results

