from pydantic import BaseModel


class CreateBookModel(BaseModel):
    title: str
    author_name: str
    author_surname: str
    year: int
    isbn: str | None = ("",)
    published_year: int | None = 0
