from fastapi import APIRouter

router = APIRouter()

@router.get("/about")
def about_page():
    return {
        "title": "О проекте ITPedia",
        "content": "ITPedia — открытая энциклопедия о технологиях, написанная сообществом."
    }

