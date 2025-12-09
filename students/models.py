from pydantic import BaseModel
from datetime import date

class InsertStudent(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    registration_date: date

class DeleteStudent(BaseModel):
    student_id: int

class Student(InsertStudent, DeleteStudent):
    pass
