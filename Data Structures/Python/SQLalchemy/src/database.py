from sqlalchemy import create_engine, text, URL, String
from config import settings
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from typing import Annotated
from sqlalchemy.orm import mapped_column

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    # pool_size=5,
    # max_overflow=10,
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)

str_256 = Annotated[str, mapped_column(String(256))]

class Base(DeclarativeBase):
    type_annotation_map = {
        str: String(256),
    }

    def __repr__(self):
        cols = []
        for col in self.__table__.columns:
            value = getattr(self, col.name, None)
            cols.append(f"{col.name}={repr(value)}")
        return f"<{self.__class__.__name__}({', '.join(cols)})>"