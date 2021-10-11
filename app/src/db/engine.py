from typing import Generator

from sqlmodel import create_engine, Session
from sqlalchemy import engine

from pyramid.config import Configurator

from app.src.config import DB_CONFIG
from app.src.logger import logger


def get_db():
    try:
        config = Configurator()
        config.scan(
            "app.src.models"
        )  # need to scan a folder and import classes and models
        engine = get_engine()
        # logger.debug("Connected to PostgreSQL database!")
    except IOError:
        logger.exception("Failed to get database connection!")
        return None, "fail"

    return engine


# define postgres sqlalchemy engine connection
def get_engine() -> engine:
    """
    Sets up database connection from config database dict.
    """
    if not (
        "db_host" in DB_CONFIG.keys()
        and "db_user" in DB_CONFIG.keys()
        and "db_password" in DB_CONFIG.keys()
        and "db_name" in DB_CONFIG.keys()
        and "db_port" in DB_CONFIG.keys()
    ):
        raise Exception("Bad config file: " + DB_CONFIG)

    url = "postgresql://{user}:{passwd}@{host}:{port}/{db}".format(
        user=DB_CONFIG["db_user"],
        passwd=DB_CONFIG["db_password"],
        host=DB_CONFIG["db_host"],
        port=DB_CONFIG["db_port"],
        db=DB_CONFIG["db_name"],
    )
    engine = create_engine(url=url, pool_size=50)
    return engine


# get engine sqlalchemy session
def get_session() -> Generator:
    engine = get_db()
    with Session(engine) as session:
        yield session


# get engine sqlmodel session
def get_session_sqlmodel():
    engine = get_db()
    session = Session(engine)
    return session
