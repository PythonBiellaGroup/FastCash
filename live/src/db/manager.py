# get session
from typing import Generator

import sqlalchemy
from live.src.db.engine import get_engine
from sqlmodel import SQLModel, Session
from live.src.logger import logger


def get_session() -> Generator:
    engine = get_engine()
    with Session(engine) as session:
        yield session


# create table
def create_table() -> bool:
    engine = get_engine()
    try:
        SQLModel.metadata.create_all(engine)
        return True
    except Exception as message:
        logger.error("non posso creare la tabella")
        logger.exception(f"errore creazione tabella: {message} ")
        raise Exception(message)


# insert_data
def insert_data(my_object: object) -> bool:
    engine = get_engine()
    logger.debug(f"Creation new object: {my_object.__str__.__name__} ")
    try:
        with Session(engine) as session:
            session.add(my_object)
            session.commit()
            session.refresh(my_object)

        return True
    except Exception as message:
        logger.error(f"non posso creare l'oggetto: {my_object.__str__.__name__}")
        logger.exception(message)
        raise Exception(message)
