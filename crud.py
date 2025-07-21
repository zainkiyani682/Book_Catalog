from fastapi import FastAPI
from pydantic import BaseModel,Field,validator
from db import engine, SessionLocal
from models import Base,Book_Catalog
from typing import Optional
from datetime import datetime
from fastapi.concurrency import run_in_threadpool
from fastapi import HTTPException

CURRENT_YEAR = datetime.now().year
app =FastAPI()

Base.metadata.create_all(bind=engine)

class BookCatalogSchema(BaseModel):
    title:str
    author:str
    published_year: int = Field(..., ge=1450, le=CURRENT_YEAR)
    summary: Optional[str] = None

    @validator('published_year')
    def validate_published_year(cls, v):
        if v < 1000 or v > 2024:
            raise ValueError('Published year must be between 1000 and 2024')
        return v

#------Create New Book --------
"""
Also There is avalidation for published year must be greater than 1450 and less than current year
-------Payload without summary:-------

{
  "title": "Test Book",
  "author": "Zain",
  "published_year": 2023
}

-------Payload with summary:-------

  {
    "title": "Learn FastApi part 2",
    "author": "Sebastián Ramírez",
    "published_year": 2016,
    "summary": "string"
  },

"""
@app.post('/books/')
def create_books(book : BookCatalogSchema):
    db=SessionLocal()
    db_books = Book_Catalog(title=book.title, author = book.author,published_year = book.published_year,summary=book.summary) 
    db.add(db_books)
    db.commit()
    db.refresh(db_books)
    db.close()
    return db_books

#-----Getting Single Book Data-----
@app.get("/books/{book_id}")
def get_item(book_id:int):
    db = SessionLocal()
    book = db.query(Book_Catalog).filter(Book_Catalog.id == book_id).first()
    db.close()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book



#-----Getting Single Book Data-----
# @app.get("/books/")
# def get_all_books():
#     db = SessionLocal()
#     books = db.query(Book_Catalog).all()
#     db.close()
#     return books

@app.get("/books/")
async def get_all_books():
    def fetch_books():
        db = SessionLocal()
        try:
            return db.query(Book_Catalog).all()
        finally:
            db.close()

    books = await run_in_threadpool(fetch_books)
    return books

#------Update Book Data-------
@app.put("/books/{book_id}")
def update_book(book_id:int, book: BookCatalogSchema):
    db=SessionLocal()
    db_book= db.query(Book_Catalog).filter(Book_Catalog.id ==book_id).first()
    if not db_book:
        db.close()
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.title=book.title
    db_book.author=book.author
    db_book.published_year=book.published_year
    db_book.summary=book.summary
    db.commit()
    db.refresh(db_book)
    db.close()
    return db_book

#-----Delete Book by id------
@app.delete('/books/{book_id}')
def delete_item(book_id:int):
    db=SessionLocal()
    db_book = db.query(Book_Catalog).filter(Book_Catalog.id == book_id).first()
    if not db_book:
        db.close()
        return {"error": "Book not found"}
    db.delete(db_book)
    db.commit()
    db.close()
    return {'message': 'Item Deleted Successfully'}
