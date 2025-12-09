from mysql.connector.connection import MySQLConnection
from .models import InsertReservation, Reservation, DeleteReservation

def get_reservations(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM reservations")
        return cursor.fetchall()
    finally:
        cursor.close()

def get_reservation(conn: MySQLConnection, payload: DeleteReservation):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM reservations WHERE reservation_id = %s", (payload.reservation_id,))
        return cursor.fetchone()
    finally:
        cursor.close()

def insert_reservation(conn: MySQLConnection, payload: InsertReservation):
    cursor = conn.cursor()
    try:
        query = """
        INSERT INTO reservations (book_id, student_id, reservation_date, status, expires_at)
        VALUES (%s, %s, %s, %s, %s)
        """
        data = payload.model_dump()
        values = (
            data["book_id"], data["student_id"], data["reservation_date"],
            data["status"], data["expires_at"]
        )
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()

def update_reservation(conn: MySQLConnection, payload: Reservation):
    cursor = conn.cursor()
    try:
        query = """
        UPDATE reservations SET book_id=%s, student_id=%s, reservation_date=%s,
                                status=%s, expires_at=%s
        WHERE reservation_id=%s
        """
        data = payload.model_dump()
        values = (
            data["book_id"], data["student_id"], data["reservation_date"],
            data["status"], data["expires_at"], data["reservation_id"]
        )
        cursor.execute(query, values)
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()

def delete_reservation(conn: MySQLConnection, payload: DeleteReservation):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM reservations WHERE reservation_id=%s", (payload.reservation_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()