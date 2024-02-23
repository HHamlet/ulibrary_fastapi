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
