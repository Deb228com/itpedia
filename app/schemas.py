# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ----------------------------
# Пользователь
# ----------------------------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


# ----------------------------
# Токен авторизации
# ----------------------------

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ----------------------------
# Статья
# ----------------------------

class ArticleBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str
    is_draft: Optional[bool] = False

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    is_draft: bool
    created_at: datetime
    updated_at: datetime
    author: UserOut

    class Config:
        orm_mode = True


# ----------------------------
# Поиск и теги (опционально)
# ----------------------------

class SearchQuery(BaseModel):
    query: str
