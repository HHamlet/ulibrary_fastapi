from fastapi import APIRouter
import books.crud as crud
from books.schemas import CreateBookModel, ShowBooks

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[ShowBooks])
async def get_book_list(page, per_page):
    return await crud.get_book_list(page, per_page)


@router.get("/title/{title}", response_model=list[ShowBooks])
async def get_books(title):
    return await crud.get_books(title=title)


@router.get("/id/{book_id}", response_model=ShowBooks | None)
async def get_book_by_id(book_id: int):
    return await crud.get_book_by_id(book_id)


@router.post("/add_book/")
async def create_book_entity(book: CreateBookModel):
    return await crud.create_book_entity(book)
