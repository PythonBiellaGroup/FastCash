# database manager functions to interact with database

from sqlmodel import Session
from sqlmodel.main import SQLModel

from app.src.db.engine import get_db
from app.src.logger import logger


# create table
def create_table(your_object: object) -> bool:
    # Database Engine
    db_engine = get_db()
    new_table = your_object
    logger.debug(f"Creating new table: {new_table}")

    try:
        SQLModel.metadata.create_all(db_engine)
        return True
    except Exception as message:
        logger.error(
            "Impossible to create the table for the object: {new_table.__class__.__name__}"
        )
        logger.exception(message)
        return False


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
        return False


# get schema
# get info (select)
# get all (select *)
# update single row
# delete single row
