from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from app.db import users_db
from app.utils.auth import hash_password, verify_password, create_session
from starlette.status import HTTP_303_SEE_OTHER

router = APIRouter()

@router.get("/login")
def login_page():
    return {"page": "login"}

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), request: Request = None):
    user = users_db.get(username)
    if not user or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    
    response = RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)
    create_session(response, username)
    return response

@router.get("/register")
def register_page():
    return {"page": "register"}

@router.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    users_db[username] = {
        "username": username,
        "password": hash_password(password),
        "articles": []
    }
    return RedirectResponse(url="/login", status_code=HTTP_303_SEE_OTHER)
