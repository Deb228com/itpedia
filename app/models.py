# app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, Table, DateTime, func
from sqlalchemy.orm import relationship, declarative_base
from passlib.context import CryptContext

Base = declarative_base()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Таблица для связи "многие ко многим" между статьями и тегами
article_tags = Table(
    "article_tags",
    Base.metadata,
    Column("article_id", ForeignKey("articles.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)

# Модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    articles = relationship("Article", back_populates="author")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str):
        self.hashed_password = pwd_context.hash(password)

# Модель статьи
class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    is_draft = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="articles")

    tags = relationship("Tag", secondary=article_tags, back_populates="articles")

# Модель тега
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    articles = relationship("Article", secondary=article_tags, back_populates="tags")
