from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection
from mysql.connector.connection import MySQLConnection
from .models import InsertBook, Book, DeleteBook
from .services import get_books, get_book, insert_book, update_book, delete_book

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[Book])
def api_get_books(conn: MySQLConnection = Depends(get_db_connection)):
    return get_books(conn)

@router.get("/{book_id}", response_model=Book)
def api_get_book(book_id: int, conn: MySQLConnection = Depends(get_db_connection)):
    book = get_book(conn, DeleteBook(book_id=book_id))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=dict)
def api_insert_book(payload: InsertBook, conn: MySQLConnection = Depends(get_db_connection)):
    return {"id": insert_book(conn, payload)}

@router.patch("/", response_model=dict)
def api_update_book(payload: Book, conn: MySQLConnection = Depends(get_db_connection)):
    rows = update_book(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="Book not found for update")
    return {"rows": rows}

@router.delete("/", response_model=dict)
def api_delete_book(payload: DeleteBook, conn: MySQLConnection = Depends(get_db_connection)):
    rows = delete_book(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="Book not found for deletion")
    return {"rows": rows}