from typing import Union
from fastapi import APIRouter
import book_copy.crud as crud
from authors.schemas import ShowAuthor
from book_copy.schemas import ShowBooksCopy

router = APIRouter(prefix="/book_copy", tags=["Book Copy"])


@router.get("/full", response_model=list[list[Union[ShowBooksCopy, ShowAuthor]]])
async def get_book_copies_full(order_by: int | int = 1):
    return await crud.get_book_copies_full(order_by=int(order_by))


@router.get("/")
async def get_book_copy(book_copy_id):
    return await crud.get_book_copy(book_copy_id)


@router.get("/{book_id}")
async def get_book_copies(book_id):
    return await crud.get_book_copies(book_id)


@router.get("/{isbn}", response_model=list[ShowBooksCopy])
async def get_by_isbn(isbn: str):
    return await crud.get_by_isbn(isbn)
