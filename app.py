from fastapi import FastAPI
import uvicorn
from books.views import router as books_router
from authors.views import router as author_router
from students.view import router as student_router
from book_copy.view import router as bc_router
from borrow.view import router as borrow_router

app = FastAPI(title="Library model on FastAPI")
app.include_router(books_router)
app.include_router(author_router)
app.include_router(student_router)
app.include_router(bc_router)
app.include_router(borrow_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
