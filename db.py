from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import CONNECTION_STRING

engine = create_async_engine(CONNECTION_STRING, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)
