# app/schemas.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ======== Пользователи ========

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


# ======== Статьи ========

class ArticleBase(BaseModel):
    title: str
    content: str

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True


# ======== Черновики ========

class DraftBase(BaseModel):
    title: str
    content: str

class DraftCreate(DraftBase):
    pass

class DraftResponse(DraftBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author: UserResponse

    class Config:
        orm_mode = True

