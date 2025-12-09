from mysql.connector.connection import MySQLConnection
from .models import CreateFine, UpdateFineStatus

def create_fine(conn: MySQLConnection, payload: CreateFine):
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO fines (transaction_id, fine_amount, calculated_date, payment_status)
        VALUES (%s, %s, %s, %s)
        """
        values = (payload.transaction_id, payload.fine_amount, payload.calculated_date, "Unpaid")
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()

def get_fines_by_student(conn: MySQLConnection, student_id: int):
    cursor = conn.cursor(dictionary=True)
    try:
        query = """
        SELECT f.* FROM fines f
        JOIN borrow_transactions bt ON f.transaction_id = bt.transaction_id
        WHERE bt.student_id = %s
        """
        cursor.execute(query, (student_id,))
        return cursor.fetchall()
    finally:
        cursor.close()

def update_fine_status(conn: MySQLConnection, payload: UpdateFineStatus):
    cursor = conn.cursor()
    try:
        query = """
        UPDATE fines
        SET payment_status = %s, paid_date = %s
        WHERE fine_id = %s
        """
        values = (payload.payment_status, payload.paid_date, payload.fine_id)
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()