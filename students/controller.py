from fastapi import APIRouter, Depends
from database import get_db_connection
from mysql.connector.connection import MySQLConnection

from .models import InsertStudent, DeleteStudent, Student
from .services import (
    get_students, get_student, insert_student,
    update_student, delete_student
)

router = APIRouter(prefix="/students", tags=["Students"])

@router.get("/")
def api_get_students(conn: MySQLConnection = Depends(get_db_connection)):
    return get_students(conn)

@router.post("/id")
def api_get_student(payload: DeleteStudent, conn: MySQLConnection = Depends(get_db_connection)):
    return get_student(conn, payload)

@router.post("/")
def api_insert_student(payload: InsertStudent, conn: MySQLConnection = Depends(get_db_connection)):
    new_id = insert_student(conn, payload)
    return {"message": "Student added", "id": new_id}

@router.patch("/")
def api_update_student(payload: Student, conn: MySQLConnection = Depends(get_db_connection)):
    count = update_student(conn, payload)
    return {"message": "Updated", "rows": count}

@router.delete("/")
def api_delete_student(payload: DeleteStudent, conn: MySQLConnection = Depends(get_db_connection)):
    count = delete_student(conn, payload)
    return {"message": "Deleted", "rows": count}
