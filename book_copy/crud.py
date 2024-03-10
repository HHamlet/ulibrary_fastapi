from sqlalchemy import select
import helper
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
