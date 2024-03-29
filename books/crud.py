from sqlalchemy import select
from db import async_session
from models import BookModel, AuthorModel, BookAuthorModel, Book_CopiesModel
from books.schemas import CreateBookModel
import helper


async def get_books(title):
    statement = select(BookModel).where(BookModel.title.like("%" + title + "%"))
    result = await helper.get_request_all(statement)
    return result


async def get_book_list(page: int = 1, per_page: int = 10):
    paginate = helper.Paginate(page=page, per_page=per_page)
    result = await helper.pagination(paginate, BookModel)
    return result


async def get_book(title):
    statement = select(BookModel).where(BookModel.title == title)
    result = await helper.get_request_one(statement)
    return result


async def get_book_by_id(book_id):
    statement = select(BookModel).where(BookModel.id == book_id)
    result = await helper.get_request_one(statement)
    return result


async def get_author(name, lastname):
    statement = select(AuthorModel).where(
        AuthorModel.first_name == name, AuthorModel.last_name == lastname
    )
    result = await helper.get_request_one(statement)
    return result


async def create_book_entity(book: CreateBookModel):
    author_res = await get_author(book.author_name, book.author_surname)
    book_res = await get_book(book.title)
    async with async_session() as session:
        async with session.begin():
            if (book_res is None) and (author_res is None):
                statement_book = BookModel(
                    title=book.title, year_first_published=book.year
                )
                statement_author = AuthorModel(
                    first_name=book.author_name, last_name=book.author_surname
                )
                session.add_all([statement_book, statement_author])
                await session.flush()
                statement_book_author = BookAuthorModel(
                    author_id=statement_author.id, book_id=statement_book.id
                )
                session.add(statement_book_author)
                statement_book_copies = Book_CopiesModel(
                    book_id=statement_book.id,
                    isbn=book.isbn,
                    year=book.published_year,
                    price=book.price,
                )
                session.add(statement_book_copies)
                await session.commit()
            elif (book_res is None) and (author_res is not None):
                statement_book = BookModel(
                    title=book.title, year_first_published=book.year
                )
                session.add(statement_book)
                await session.commit()
                statement_book_author = BookAuthorModel(
                    author_id=author_res.id, book_id=statement_book.id
                )
                statement_book_copies = Book_CopiesModel(
                    book_id=statement_book.id,
                    isbn=book.isbn,
                    year=book.published_year,
                    price=book.price,
                )
                session.add_all([statement_book_author, statement_book_copies])
                await session.commit()
            elif (book_res is not None) and (author_res is None):
                statement_author = AuthorModel(
                    first_name=book.author_name, last_name=book.author_surname
                )
                session.add(statement_author)
                await session.commit()
                statement_book_author = BookAuthorModel(
                    author_id=statement_author.id, book_id=book_res.id
                )
                statement_book_copies = Book_CopiesModel(
                    book_id=book_res.id,
                    isbn=book.isbn,
                    year=book.published_year,
                    price=book.price,
                )
                session.add_all([statement_book_author, statement_book_copies])
                await session.commit()
            else:
                statement_book_copies = Book_CopiesModel(
                    book_id=book_res.id,
                    isbn=book.isbn,
                    year=book.published_year,
                    price=book.price,
                )
                session.add(statement_book_copies)
                await session.commit()
