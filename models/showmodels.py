from pydantic import BaseModel, EmailStr


class ShowBooks(BaseModel):
    id: int
    title: str
    year_first_published: int


class ShowBooksCopy(BaseModel):
    id: int
    isbn: str
    year: int
    book: ShowBooks
    price: int | None = 0


class ShowAuthor(BaseModel):
    id: int
    first_name: str
    last_name: str


class ShowStudent(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
