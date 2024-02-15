from fastapi import FastAPI
import uvicorn
from sqlalchemy import select
from models import (
    BookModel,
    BookAuthorModel,
    AuthorModel,
    Book_CopiesModel,
    ShowBooks,
    ShowAuthor,
)
from db import async_session

app = FastAPI(title="Library model on FastAPI")


async def get_request(statement):
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.all()
        return result


async def get_book(title):
    statement = select(BookModel).where(BookModel.title == title)
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.first()
    return result


@app.get("/books", response_model=list[ShowBooks])
async def get_book_list():
    statement = select(BookModel)
    result = await get_request(statement)
    return result


@app.get("/books/{title}", response_model=list[ShowBooks])
async def get_books(title):
    statement = select(BookModel).where(BookModel.title.like("%" + title + "%"))
    result = await get_request(statement)
    return result


@app.post("/books/add_book")
async def create_book_entity(
    title,
    author_name,
    author_surname,
    year: int,
    isbn: str | None = "",
    published_year: int | None = 0,
):
    author_res = await get_author(author_name, author_surname)
    book_res = await get_book(title)
    async with async_session() as session:
        async with session.begin():
            if (book_res is None) and (author_res is None):
                statement_book = BookModel(title=title, year_first_published=year)
                statement_author = AuthorModel(
                    first_name=author_name, last_name=author_surname
                )
                session.add_all([statement_book, statement_author])
                session.commit()
                statement_book_author = BookAuthorModel(
                    author_id=statement_author.id, book_id=statement_book.id
                )
                session.add(statement_book_author)
                statement_book_copies = Book_CopiesModel(
                    book_id=statement_book.id, isbn=isbn, year=published_year
                )
                session.add(statement_book_copies)
                session.commit()
            elif (book_res is None) and (author_res is not None):
                statement_book = BookModel(title=title, year_first_published=year)
                session.add(statement_book)
                session.commit()
                statement_book_author = BookAuthorModel(
                    author_id=author_res.id, book_id=statement_book.id
                )
                statement_book_copies = Book_CopiesModel(
                    book_id=statement_book.id, isbn=isbn, year=published_year
                )
                session.add_all([statement_book_author, statement_book_copies])
                session.commit()
            elif (book_res is not None) and (author_res is None):
                statement_author = AuthorModel(
                    first_name=author_name, last_name=author_surname
                )
                session.add(statement_author)
                session.commit()
                statement_book_author = BookAuthorModel(
                    author_id=statement_author.id, book_id=book_res.id
                )
                statement_book_copies = Book_CopiesModel(
                    book_id=book_res.id, isbn=isbn, year=published_year
                )
                session.add_all([statement_book_author, statement_book_copies])
                session.commit()
            else:
                statement_book_copies = Book_CopiesModel(
                    book_id=book_res.id, isbn=isbn, year=published_year
                )
                session.add(statement_book_copies)
                session.commit()


@app.get("/authors_books")
async def get_author_books():
    statement = select(BookAuthorModel)
    result = await get_request(statement)
    return result


@app.get("/author", response_model=list[ShowAuthor])
async def get_author(name, lastname):
    statement = select(AuthorModel).where(
        AuthorModel.first_name == name, AuthorModel.last_name == lastname
    )
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.first()
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
