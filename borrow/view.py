from fastapi import APIRouter
import borrow.crud as crud

router = APIRouter(prefix="/borrow", tags=["Borrow"])


@router.get("/")
async def check_book_in_borrow_table(book_copy_id):
    return await crud.check_book_in_borrow_table(book_copy_id)


@router.post("/")
async def borrow_to(book_copy_id, student_id):
    return await crud.borrow_to(book_copy_id, student_id)
