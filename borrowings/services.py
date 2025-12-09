from mysql.connector.connection import MySQLConnection
from .models import InsertBorrowTransaction, BorrowTransaction, DeleteBorrowTransaction

def get_borrow_transactions(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM borrow_transactions")
        return cursor.fetchall()
    finally:
        cursor.close()

def get_borrow_transaction(conn: MySQLConnection, payload: DeleteBorrowTransaction):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM borrow_transactions WHERE transaction_id = %s", (payload.transaction_id,))
        return cursor.fetchone()
    finally:
        cursor.close()

def insert_borrow_transaction(conn: MySQLConnection, payload: InsertBorrowTransaction):
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO borrow_transactions (book_id, student_id, librarian_id, borrow_date,
                                         due_date, return_date, status, is_overdue)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        data = payload.model_dump()
        values = (
            data["book_id"], data["student_id"], data["librarian_id"],
            data["borrow_date"], data["due_date"], data["return_date"],
            data["status"], data["is_overdue"]
        )
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()

def update_borrow_transaction(conn: MySQLConnection, payload: BorrowTransaction):
    cursor = conn.cursor()
    try:
        query = """
        UPDATE borrow_transactions SET book_id=%s, student_id=%s, librarian_id=%s,
                                       borrow_date=%s, due_date=%s, return_date=%s,
                                       status=%s, is_overdue=%s
        WHERE transaction_id=%s
        """
        data = payload.model_dump()
        values = (
            data["book_id"], data["student_id"], data["librarian_id"],
            data["borrow_date"], data["due_date"], data["return_date"],
            data["status"], data["is_overdue"], data["transaction_id"]
        )
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()

def delete_borrow_transaction(conn: MySQLConnection, payload: DeleteBorrowTransaction):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM borrow_transactions WHERE transaction_id=%s", (payload.transaction_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()