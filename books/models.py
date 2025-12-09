from pydantic import BaseModel
from datetime import date

class InsertBook(BaseModel):
    isbn: str | None = None
    title: str
    author: str
    publisher: str | None = None
    publication_year: int | None = None
    category: str | None = None
    location: str | None = None
    quantity: int
    status: str = "Available"
    date_added: date

class DeleteBook(BaseModel):
    book_id: int

class Book(InsertBook, DeleteBook):
    pass
