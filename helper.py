import math
from typing import Annotated
from fastapi.param_functions import Query
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from db import async_session


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


async def pagination(paginate: Annotated[Paginate, Depends(pagination_param)], dbmodel):
    offset = (paginate.page - 1) * paginate.per_page
    statement = select(dbmodel).limit(int(paginate.per_page)).offset(offset)
    result = await get_request_all(statement)
    # total_page = math.ceil(
    #     len(await get_request_all(select(dbmodel))) / int(paginate.per_page)
    # )
    return result
