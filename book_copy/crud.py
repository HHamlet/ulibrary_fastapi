from sqlalchemy import select

from books.crud import get_request
from db import async_session
from models.book_copies import Book_CopiesModel


async def get_book_copy(book_copy_id):
    statement = select(Book_CopiesModel).where(Book_CopiesModel.id == int(book_copy_id))
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.first()
        return result


async def get_book_copies(book_id):
    statement = select(Book_CopiesModel).where(Book_CopiesModel.book_id == int(book_id))
    result = await get_request(statement)
    return result
