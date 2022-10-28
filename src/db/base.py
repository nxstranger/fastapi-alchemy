import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import as_declarative
from ..settings import settings


DB_PASS = settings.DB_PASS
DB_USER = settings.DB_USER
DB_NAME = settings.DB_NAME
DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT

engine = create_engine(
    "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
        DB_USER,
        DB_PASS,
        DB_HOST,
        DB_PORT,
        DB_NAME
    ),
    isolation_level="REPEATABLE READ",
    echo=True,
)
Session = sessionmaker()
current_session = scoped_session(Session)


metadata = MetaData(bind=engine)


@as_declarative(metadata=metadata)
class Base:
    pass

