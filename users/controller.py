from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection
from mysql.connector.connection import MySQLConnection
from .models import RegisterUser, LoginUser, DeleteUser
from .services import register_user, authenticate_user, delete_user
from .models import UpdateUser, User
from .services import get_user_by_id, update_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=dict)
def api_register_user(payload: RegisterUser, conn: MySQLConnection = Depends(get_db_connection)):
    user_id = register_user(conn, payload)
    return {"id": user_id}

@router.post("/login", response_model=dict)
def api_login_user(payload: LoginUser, conn: MySQLConnection = Depends(get_db_connection)):
    user = authenticate_user(conn, payload)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # TODO: issue JWT token here
    return {"message": "Login successful", "user_id": user["user_id"], "user_type": user["user_type"]}

@router.delete("/", response_model=dict)
def api_delete_user(payload: DeleteUser, conn: MySQLConnection = Depends(get_db_connection)):
    rows = delete_user(conn, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"rows": rows}

@router.get("/{user_id}", response_model=User)
def api_get_user(user_id: int, conn: MySQLConnection = Depends(get_db_connection)):
    user = get_user_by_id(conn, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=dict)
def api_update_user(
    user_id: int,
    payload: UpdateUser,
    conn: MySQLConnection = Depends(get_db_connection)
):
    rows = update_user(conn, user_id, payload)
    if rows == 0:
        raise HTTPException(status_code=404, detail="No changes made or user not found")
    return {"rows_updated": rows}