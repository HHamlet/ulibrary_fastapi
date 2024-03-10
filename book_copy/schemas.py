from pydantic import BaseModel
from books.schemas import ShowBooks


class ShowBooksCopy(BaseModel):
    id: int
    isbn: str
    year: int
    book: ShowBooks
    price: int | None = 0
