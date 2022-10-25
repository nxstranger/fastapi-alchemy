import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.declarative import as_declarative

DB_PASS = os.environ.get('DB_PASS', 'postgres')
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', 5432)

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

metadata = MetaData(bind=engine)


@as_declarative(metadata=metadata)
class Base:
    pass

