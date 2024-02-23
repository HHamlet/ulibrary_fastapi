from sqlalchemy import select
import helper
from models import BookAuthorModel, AuthorModel


async def get_author_books():
    statement = select(BookAuthorModel)
    result = await helper.get_request_all(statement)
    return result


async def get_author(name, lastname):
    statement = select(AuthorModel).where(
        AuthorModel.first_name == name, AuthorModel.last_name == lastname
    )
    result = await helper.get_request_one(statement)
    return result
