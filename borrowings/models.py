from pydantic import BaseModel
from datetime import date, datetime

class InsertBorrowTransaction(BaseModel):
    book_id: int
    student_id: int
    librarian_id: int
    borrow_date: date
    due_date: date
    return_date: date | None = None
    status: str = "Active"   # enum: Active, Returned, Overdue
    is_overdue: bool = False

class DeleteBorrowTransaction(BaseModel):
    transaction_id: int

class BorrowTransaction(InsertBorrowTransaction, DeleteBorrowTransaction):
    created_at: datetime | None = None