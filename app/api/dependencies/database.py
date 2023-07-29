from sqlmodel import SQLModel, Session, create_engine

from databases import Database

DATABASE_URL = 'postgresql://postgres:postgrespw@localhost:49154/gpc_dev'

database = Database(DATABASE_URL)

engine = create_engine(DATABASE_URL)


# def init_db():
#     SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as connection:
        yield connection
