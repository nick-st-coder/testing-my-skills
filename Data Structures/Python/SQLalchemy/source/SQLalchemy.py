from sqlalchemy import create_engine, text, URL
from config import settings
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import asyncio

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
    # pool_size=5,
    # max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
)

# with sync_engine.connect() as connection:
#     res = connection.execute (text("SELECT 1,2,3 union SELECT 4,5,6"))
#     print (f"{res.all()=}")

async def get_async_session():  
    async with async_engine.connect() as connection:
        res = await connection.execute(text("SELECT 1,2,3 union SELECT 4,5,6"))
        print(f"{res.all()=}")

asyncio.run(get_async_session())