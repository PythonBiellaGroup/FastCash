# database manager functions to interact with database
from sqlalchemy.orm.session import sessionmaker
from sqlmodel import Session
from sqlmodel.main import SQLModel

from app.src.db.engine import get_db
from app.src.logger import logger


# get engine sqlalchemy session
def get_session():
    engine = get_db()
    # Session = sessionmaker(engine)
    session = Session(engine)
    return session


# create table
def create_table() -> bool:
    # Database Engine
    db_engine = get_db()
    try:
        # for table in objects:
        #     new_table = table
        #     logger.debug(f"Creating new table: {new_table}")
        SQLModel.metadata.create_all(db_engine)
        return True
    except Exception as message:
        logger.error(
            "Impossible to create the table for the object: {new_table.__class__.__name__}"
        )
        logger.exception(message)
        raise Exception(message)


# Destroy metadata table
def destroy_metadata_table() -> bool:
    # Database Engine
    db_engine = get_db()
    try:
        # for table in objects:
        #     new_table = table
        #     logger.debug(f"Creating new table: {new_table}")
        SQLModel.metadata.drop_all(db_engine)
        return True
    except Exception as message:
        logger.error(
            "Impossible to create the table for the object: {new_table.__class__.__name__}"
        )
        logger.exception(message)
        raise Exception(message)


# check table
def check_table():
    pass


# insert new table with data
def insert_data(your_object: object) -> bool:
    # Database Engine
    db_engine = get_db()
    logger.debug(f"Creating new table: {logger}")
    try:
        with Session(db_engine) as session:
            session.add(your_object)
            session.commit()
        return True
    except Exception as message:
        logger.error(
            "Impossible to create the table for the object: {your_object.__class__.__name__}"
        )
        logger.exception(message)
        raise Exception(message)


# refresh the schema and data
def refresh_data(your_object: object) -> bool:
    db_engine = get_db()
    try:
        with Session(db_engine) as session:
            session.refresh(your_object)
        return True
    except Exception as message:
        logger.error(
            "Impossible to refresh the object: {your_object.__class__.__name__}"
        )
        logger.exception(message)
        raise Exception(message)


# get schema
# get info (select)
# get all (select *)
# update single row
# delete single row
