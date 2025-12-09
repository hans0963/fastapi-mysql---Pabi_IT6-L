from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection
from mysql.connector.connection import MySQLConnection
from .models import InsertBorrowTransaction, BorrowTransaction, DeleteBorrowTransaction
from .services import (
    get_borrow_transactions,
    get_borrow_transaction,
    insert_borrow_transaction,
    update_borrow_transaction,
    delete_borrow_transaction
)

router = APIRouter(prefix="/borrow-transactions", tags=["Borrow Transactions"])

@router.get("/", response_model=list[BorrowTransaction])
def api_get_borrow_transactions(conn: MySQLConnection = Depends(get_db_connection)):
    return get_borrow_transactions(conn)

@router.get("/{transaction_id}", response_model=BorrowTransaction)
def api_get_borrow_transaction(transaction_id: int, conn: MySQLConnection = Depends(get_db_connection)):
    transaction = get_borrow_transaction(conn, DeleteBorrowTransaction(transaction_id=transaction_id))
    if not transaction:
        raise HTTPException(status_code=404, detail="Borrow transaction not found")
    return transaction

@router.post("/", response_model=dict)
def api_insert_borrow_transaction(payload: InsertBorrowTransaction, conn: MySQLConnection = Depends(get_db_connection)):
    return {"id": insert_borrow_transaction(conn, payload)}

@router.patch("/", response_model=dict)
def api_update_borrow_transaction(payload: BorrowTransaction, conn: MySQLConnection = Depends(get_db_connection)):
    rows = update_borrow_transaction(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="Borrow transaction not found for update")
    return {"rows": rows}

@router.delete("/", response_model=dict)
def api_delete_borrow_transaction(payload: DeleteBorrowTransaction, conn: MySQLConnection = Depends(get_db_connection)):
    rows = delete_borrow_transaction(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="Borrow transaction not found for deletion")
    return {"rows": rows}