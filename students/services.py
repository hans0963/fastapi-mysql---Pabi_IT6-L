from mysql.connector.connection import MySQLConnection
from .models import InsertStudent, Student, DeleteStudent

def get_students(conn: MySQLConnection):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()

def get_student(conn: MySQLConnection, payload: DeleteStudent):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students WHERE student_id = %s", (payload.student_id,))
    return cursor.fetchone()

def insert_student(conn: MySQLConnection, payload: InsertStudent):
    cursor = conn.cursor()
    query = """
    INSERT INTO students (first_name, last_name, email, phone, registration_date)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        payload.first_name,
        payload.last_name,
        payload.email,
        payload.phone,
        payload.registration_date
    )
    cursor.execute(query, values)
    conn.commit()
    return cursor.lastrowid

def update_student(conn: MySQLConnection, payload: Student):
    cursor = conn.cursor()
    query = """
    UPDATE students SET first_name=%s, last_name=%s, email=%s, phone=%s, registration_date=%s
    WHERE student_id=%s
    """
    values = (
        payload.first_name,
        payload.last_name,
        payload.email,
        payload.phone,
        payload.registration_date,
        payload.student_id
    )
    cursor.execute(query, values)
    conn.commit()
    return cursor.rowcount

def delete_student(conn: MySQLConnection, payload: DeleteStudent):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE student_id = %s", (payload.student_id,))
    conn.commit()
    return cursor.rowcount
