from fastapi import FastAPI
import uvicorn
from sqlalchemy import select
from models import BookModel, BookAuthorModel, AuthorModel
from db import async_session

app = FastAPI(title="Library model on FastAPI")


async def get_request(statement):
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.all()
        return result


@app.get("/books")
async def get_book_list():
    statement = select(BookModel)
    result = await get_request(statement)
    return result


@app.get("/books/{title}")
async def get_book(title):
    statement = select(BookModel).where(BookModel.title.like("%" + title + "%"))
    result = await get_request(statement)
    return result


@app.get("/authors_books")
async def get_author_books():
    statement = select(BookAuthorModel)
    result = await get_request(statement)
    return result


@app.get("/author")
async def get_author(name, lastname):
    statement = select(AuthorModel).where(
        AuthorModel.first_name == name, AuthorModel.last_name == lastname
    )
    result = await get_request(statement)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
