from app.utils.auth import auth_required

@router.get("/create", response_class=HTMLResponse)
@auth_required
async def create_article_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})
