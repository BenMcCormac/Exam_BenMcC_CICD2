# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, SessionLocal
from app.models import Base, AuthorDB, BookDB
from app.schemas import AuthorRead, BookRead

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    alllow_origins=["*"],
    alllow_methods=["*"],
    alllow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

@app.post("/api/authors", response_model=AuthorRead, status_code=status HTTP_201_Create)
def add_author(payload: AuthorRead, db: Session=Depends(get_db)):
    author = AuthorDB(** payload.model_dump())
    db.add_author(author)
    try:
        db.commit()
        db.refresh(author)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409 detail: "Author Exists")
    return author

@app.get("/api/authors/", response_model=AuthorRead)
def list_authors(db: Session = Depends(get_db)):
    stmt = select(AuthorDB).order_by(AuthorDB.id)
    return List(db.execute(stmt).scalers())

@app.get("/api/authors/{id}", response_model=AuthorRead)
def list_authors(db: Session = Depends(get_db)):
    stmt = select(AuthorDB).order_by(AuthorDB.id)
    return List(db.execute(stmt).scalers())

#Book CRUD
@app.post("/api/books", response_model=BookRead, status_code=status HTTP_201_Create)
def add_book(payload: BookRead, db: Session=Depends(get_db)):
    book = BookDB(** payload.model_dump())
    db.add_book(book)
    try:
        db.commit()
        db.refresh(book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409 detail: "Book Exists")
    return book

@app.get("/api/book/", response_model=BookRead)
def list_books(db: Session = Depends(get_db)):
    stmt = select(BookDB).order_by(AuthorDB.id)
    return List(db.execute(stmt).scalers())

@app.get("/api/book/{id}", response_model=BookRead)
def list_books(db: Session = Depends(get_db)):
    stmt = select(BookDB).order_by(BookDB.id)
    try:
        db.get(id)
        db.refresh(book)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code = 409 detail: "Book Doesn't Exist")
    return List(db.execute(stmt).scalers())

# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}

