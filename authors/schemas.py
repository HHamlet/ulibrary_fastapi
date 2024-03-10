from pydantic import BaseModel


class ShowAuthor(BaseModel):
    id: int
    first_name: str
    last_name: str
