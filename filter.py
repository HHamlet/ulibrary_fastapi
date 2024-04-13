import asyncio
from sqlalchemy import select
from db import async_session
from models import Book_CopiesModel, AuthorModel, BookAuthorModel, BookModel


async def filter_by_author(first_name: str, last_name: str | None = ""):

    statement = (
        select(
            Book_CopiesModel,
            AuthorModel,
        )
        .select_from(AuthorModel)
        .join(BookAuthorModel, AuthorModel.id == BookAuthorModel.author_id)
        .join(BookModel, BookAuthorModel.book_id == BookModel.id)
        .join(Book_CopiesModel, BookModel.id == Book_CopiesModel.book_id)
        .where(AuthorModel.first_name == first_name, AuthorModel.last_name == last_name)
    )
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(statement)
            rows = result.fetchall()
    return rows


async def filter_by_isbn(isbn: str):

    statement = (
        select(
            Book_CopiesModel,
            AuthorModel,
        )
        .select_from(AuthorModel)
        .join(BookAuthorModel, AuthorModel.id == BookAuthorModel.author_id)
        .join(BookModel, BookAuthorModel.book_id == BookModel.id)
        .join(Book_CopiesModel, BookModel.id == Book_CopiesModel.book_id)
        .where(Book_CopiesModel.isbn == isbn)
    )
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(statement)
            rows = result.fetchall()
    return rows


async def filter_by_price(p_min: int | None = 0, p_max: int | None = 50):

    statement = (
        select(
            Book_CopiesModel,
            AuthorModel,
        )
        .select_from(AuthorModel)
        .join(BookAuthorModel, AuthorModel.id == BookAuthorModel.author_id)
        .join(BookModel, BookAuthorModel.book_id == BookModel.id)
        .join(Book_CopiesModel, BookModel.id == Book_CopiesModel.book_id)
        .order_by(Book_CopiesModel.price)
    )
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(statement)
            rows = result.fetchall()
    filtered_rows = [row for row in rows if p_min <= row[0].price <= p_max]
    return filtered_rows


# asyncio.run(filter_by_author("Aditya", "Bhagrava"))
# asyncio.run(filter_by_isbn("1617292230"))
asyncio.run(filter_by_price())
