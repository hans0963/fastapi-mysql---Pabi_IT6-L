from pydantic import BaseModel
from datetime import date, datetime

class InsertReservation(BaseModel):
    book_id: int
    student_id: int
    reservation_date: date
    status: str = "Active"   # enum: Active, Fulfilled, Cancelled
    expires_at: datetime | None = None

class DeleteReservation(BaseModel):
    reservation_id: int

class Reservation(InsertReservation, DeleteReservation):
    created_at: datetime | None = None