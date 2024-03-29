from pydantic import BaseModel


class CreateBookModel(BaseModel):
    title: str
    author_name: str
    author_surname: str
    year: int
    isbn: str | None = ""
    published_year: int | None = 0
    price: int | None = 0


class ShowBooks(BaseModel):
    id: int
    title: str
    year_first_published: int
