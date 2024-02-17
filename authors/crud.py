from sqlalchemy import select

from books.crud import get_request
from db import async_session
from models import BookAuthorModel, AuthorModel


async def get_author_books():
    statement = select(BookAuthorModel)
    result = await get_request(statement)
    return result


async def get_author(name, lastname):
    statement = select(AuthorModel).where(
        AuthorModel.first_name == name, AuthorModel.last_name == lastname
    )
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.first()
    return result
