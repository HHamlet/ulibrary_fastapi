from sqlalchemy import select
import helper
from db import async_session
from models import BookAuthorModel, BookModel, AuthorModel
from models.book_copies import Book_CopiesModel


async def get_book_copy(book_copy_id):
    statement = select(Book_CopiesModel).where(Book_CopiesModel.id == int(book_copy_id))
    result = await helper.get_request_one(statement)
    return result


async def get_book_copies(book_id):
    statement = select(Book_CopiesModel).where(Book_CopiesModel.book_id == int(book_id))
    result = await helper.get_request_all(statement)
    return result


async def get_by_isbn(isbn: str):
    statement = select(Book_CopiesModel).where(Book_CopiesModel.isbn == isbn)
    result = await helper.get_request_all(statement)
    return result


async def get_book_copies_full(order_by: int):
    sort_by = {
        1: Book_CopiesModel.id,
        2: AuthorModel.first_name,
        3: AuthorModel.last_name,
    }

    statement1 = (
        select(
            Book_CopiesModel,
            AuthorModel,
        )
        .select_from(AuthorModel)
        .join(BookAuthorModel, AuthorModel.id == BookAuthorModel.author_id)
        .join(BookModel, BookAuthorModel.book_id == BookModel.id)
        .join(Book_CopiesModel, BookModel.id == Book_CopiesModel.book_id)
        .order_by(sort_by[order_by])
    )
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(statement1)
            rows = result.fetchall()

    return rows
