from mysql.connector.connection import MySQLConnection
from .models import InsertBook, Book, DeleteBook

def get_books(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM books")
        return cursor.fetchall()
    finally:
        cursor.close()

def get_book(conn: MySQLConnection, payload: DeleteBook):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM books WHERE book_id = %s", (payload.book_id,))
        return cursor.fetchone()
    finally:
        cursor.close()

def insert_book(conn: MySQLConnection, payload: InsertBook):
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO books (isbn, title, author, publisher, publication_year,
                           category, location, quantity, status, date_added)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        data = payload.model_dump()
        values = (
            data["isbn"], data["title"], data["author"], data["publisher"],
            data["publication_year"], data["category"], data["location"],
            data["quantity"], data["status"], data["date_added"]
        )
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()

def update_book(conn: MySQLConnection, payload: Book):
    cursor = conn.cursor()
    try:
        query = """
        UPDATE books SET isbn=%s, title=%s, author=%s, publisher=%s,
                         publication_year=%s, category=%s, location=%s,
                         quantity=%s, status=%s, date_added=%s
        WHERE book_id=%s
        """
        data = payload.model_dump()
        values = (
            data["isbn"], data["title"], data["author"], data["publisher"],
            data["publication_year"], data["category"], data["location"],
            data["quantity"], data["status"], data["date_added"], data["book_id"]
        )
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()

def delete_book(conn: MySQLConnection, payload: DeleteBook):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM books WHERE book_id=%s", (payload.book_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()