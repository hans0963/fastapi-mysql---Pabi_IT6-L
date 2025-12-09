from pydantic import BaseModel
from datetime import date, datetime

class Fine(BaseModel):
    fine_id: int
    transaction_id: int
    fine_amount: float
    calculated_date: date
    paid_date: date | None = None
    payment_status: str = "Unpaid"
    created_at: datetime | None = None

class CreateFine(BaseModel):
    transaction_id: int
    fine_amount: float
    calculated_date: date

class UpdateFineStatus(BaseModel):
    fine_id: int
    payment_status: str   # 'Unpaid', 'Paid', 'Waived'
    paid_date: date | None = None