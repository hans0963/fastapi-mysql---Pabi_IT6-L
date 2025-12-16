from pydantic import BaseModel, EmailStr
from datetime import datetime

class RegisterUser(BaseModel):
    email: EmailStr
    password: str
    user_type: str = "student"   # student or librarian
    student_id: int | None = None

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class DeleteUser(BaseModel):
    user_id: int

class User(BaseModel):
    user_id: int
    email: EmailStr
    user_type: str
    student_id: int | None = None
    created_at: datetime | None = None
    account_status: str = "active"

class UpdateUser(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    account_status: str | None = None