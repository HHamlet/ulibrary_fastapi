from fastapi import APIRouter
import books.crud as crud
from models.showmodels import ShowBooks
from books.schemas import CreateBookModel

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=list[ShowBooks])
async def get_book_list():
    return crud.get_book_list()


@router.get("/{title}/", response_model=list[ShowBooks])
async def get_books(title):
    return crud.get_books(title=title)


@router.get("/{book_id}/", response_model=ShowBooks)
async def get_book_by_id(book_id: int):
    return crud.get_book_by_id(book_id)


@router.post("/add_book/")
async def create_book_entity(book: CreateBookModel):
    return crud.create_book_entity(book)
