from mysql.connector.connection import MySQLConnection
from .models import RegisterUser, LoginUser, DeleteUser
import bcrypt

def register_user(conn: MySQLConnection, payload: RegisterUser):
    cursor = conn.cursor()
    try:
        # Hash password
        hashed_pw = bcrypt.hashpw(payload.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        query = """
        INSERT INTO users (email, password_hash, user_type, student_id, account_status)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (payload.email, hashed_pw, payload.user_type, payload.student_id, "active")
        cursor.execute(query, values)
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()

def authenticate_user(conn: MySQLConnection, payload: LoginUser):
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE email=%s", (payload.email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(payload.password.encode("utf-8"), user["password_hash"].encode("utf-8")):
            return user
        return None
    finally:
        cursor.close()

def delete_user(conn: MySQLConnection, payload: DeleteUser):
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM users WHERE user_id=%s", (payload.user_id,))
        conn.commit()
        return cursor.rowcount
    finally:
        cursor.close()