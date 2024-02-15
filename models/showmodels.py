from pydantic import BaseModel


class ShowBooks(BaseModel):
    id: int
    title: str
    year_first_published: int


class ShowAuthor(BaseModel):
    id: int
    first_name: str
    last_name: str
