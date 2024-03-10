from fastapi import APIRouter
import book_copy.crud as crud
from book_copy.schemas import ShowBooksCopy

router = APIRouter(prefix="/book_copy", tags=["Book Copy"])


@router.get("/")
async def get_book_copy(book_copy_id):
    return await crud.get_book_copy(book_copy_id)


@router.get("/{book_id}")
async def get_book_copies(book_id):
    return await crud.get_book_copies(book_id)


@router.get("/{isbn}", response_model=list[ShowBooksCopy])
async def get_by_isbn(isbn: str):
    return await crud.get_by_isbn(isbn)
