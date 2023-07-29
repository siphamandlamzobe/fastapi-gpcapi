import os
from sqlmodel import Session, create_engine

from databases import Database

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = 'postgresql://postgres:postgrespw@localhost:49154/gpc_dev'

database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as connection:
        yield connection
