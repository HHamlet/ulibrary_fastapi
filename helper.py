import json
import math
from typing import Annotated
import redis
from fastapi.param_functions import Query
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select, inspect
from sqlalchemy.exc import NoResultFound

from db import async_session

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)


async def get_request_all(statement):
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.all()
        return result


async def get_request_one(statement):
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            try:
                result = temp.one()
            except NoResultFound:
                result = None
        return result


class Paginate(BaseModel):
    page: int
    per_page: int


async def pagination_param(
    page: int = Query(ge=1, required=False, default=1, le=5000),
    per_page: int = Query(ge=1, required=False, default=10, le=100),
):
    return Paginate(page=page, per_page=per_page)


async def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


async def pagination(paginate: Annotated[Paginate, Depends(pagination_param)], dbmodel):
    cache_name = f"{dbmodel.__name__}_{paginate.page}_{paginate.per_page}"
    pagination_result = redis_client.get(cache_name)
    if pagination_result is None:

        offset = (paginate.page - 1) * paginate.per_page
        statement = select(dbmodel).limit(int(paginate.per_page)).offset(offset)
        result = await get_request_all(statement)
        dict_books = [await object_as_dict(book) for book in result]
        print(dict_books)
        redis_client.set(cache_name, json.dumps(dict_books))
        return dict_books
    else:
        books = json.loads(pagination_result)
        print(books)
        return books
    # total_page = math.ceil(
    #     len(await get_request_all(select(dbmodel))) / int(paginate.per_page)
    # )
    # return result
