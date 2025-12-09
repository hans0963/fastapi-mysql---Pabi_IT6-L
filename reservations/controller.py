from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection
from mysql.connector.connection import MySQLConnection
from .models import InsertReservation, Reservation, DeleteReservation
from .services import (
    get_reservations,
    get_reservation,
    insert_reservation,
    update_reservation,
    delete_reservation
)

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.get("/", response_model=list[Reservation])
def api_get_reservations(conn: MySQLConnection = Depends(get_db_connection)):
    return get_reservations(conn)

@router.get("/{reservation_id}", response_model=Reservation)
def api_get_reservation(reservation_id: int, conn: MySQLConnection = Depends(get_db_connection)):
    reservation = get_reservation(conn, DeleteReservation(reservation_id=reservation_id))
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.post("/", response_model=dict)
def api_insert_reservation(payload: InsertReservation, conn: MySQLConnection = Depends(get_db_connection)):
    return {"id": insert_reservation(conn, payload)}

@router.patch("/", response_model=dict)
def api_update_reservation(payload: Reservation, conn: MySQLConnection = Depends(get_db_connection)):
    rows = update_reservation(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="Reservation not found for update")
    return {"rows": rows}

@router.delete("/", response_model=dict)
def api_delete_reservation(payload: DeleteReservation, conn: MySQLConnection = Depends(get_db_connection)):
    rows = delete_reservation(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="Reservation not found for deletion")
    return {"rows": rows}