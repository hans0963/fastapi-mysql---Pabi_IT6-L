from fastapi import FastAPI


from students.controller import router as students_router
from books.controller import router as books_router
from borrowings.controller import router as borrowings_router
from reservations.controller import router as reservations_router
from users.controller import router as users_router
from fines.controller import router as fines_router


def register_routes(app: FastAPI):
    app.include_router(students_router, prefix="/api/v1")
    app.include_router(books_router, prefix="/api/v1")
    app.include_router(borrowings_router, prefix="/api/v1")
    app.include_router(reservations_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(fines_router, prefix="/api/v1")