# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# ----------------------------
# Схемы пользователя
# ----------------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


# ----------------------------
# Схемы статьи
# ----------------------------

class ArticleBase(BaseModel):
    title: str
    content: str
    is_draft: bool = False
    category: Optional[str] = None
    tags: Optional[List[str]] = []

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
