from fastapi import APIRouter
import book_copy.crud as crud

router = APIRouter(prefix="/book_copy", tags=["Book Copy"])


@router.get("/")
async def get_book_copy(book_copy_id):
    return await crud.get_book_copy(book_copy_id)


@router.get("/{book_id}")
async def get_book_copies(book_id):
    return await crud.get_book_copies(book_id)
