from fastapi import APIRouter, Depends, HTTPException
from mysql.connector.connection import MySQLConnection
from database import get_db_connection
from .models import CreateFine, UpdateFineStatus
from .services import create_fine, get_fines_by_student, update_fine_status
from .services import get_all_fines, get_fine_by_id
from .models import Fine

router = APIRouter(prefix="/fines", tags=["Fines"])

@router.post("/", response_model=dict)
def api_create_fine(payload: CreateFine, conn: MySQLConnection = Depends(get_db_connection)):
    fine_id = create_fine(conn, payload)
    return {"fine_id": fine_id}

@router.get("/student/{student_id}", response_model=list)
def api_get_fines(student_id: int, conn: MySQLConnection = Depends(get_db_connection)):
    fines = get_fines_by_student(conn, student_id)
    if not fines:
        raise HTTPException(status_code=404, detail="No fines found for this student")
    return fines

@router.put("/", response_model=dict)
def api_update_fine(payload: UpdateFineStatus, conn: MySQLConnection = Depends(get_db_connection)):
    rows = update_fine_status(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="Fine not found")
    return {"rows_updated": rows}

@router.get("/", response_model=list[Fine])
def api_get_all_fines(conn: MySQLConnection = Depends(get_db_connection)):
    return get_all_fines(conn)

@router.get("/{fine_id}", response_model=Fine)
def api_get_fine_by_id(fine_id: int, conn: MySQLConnection = Depends(get_db_connection)):
    fine = get_fine_by_id(conn, fine_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return fine