from typing import Generator

# Async flavour
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from pyramid.config import Configurator

from app.src.config import DB_CONFIG
from app.src.logger import logger


async def get_db():
    try:
        config = Configurator()
        config.scan(
            "app.src.models"
        )  # need to scan a folder and import classes and models
        engine = await get_engine()
        logger.info("Connected to PostgreSQL database!")
    except IOError:
        logger.exception("Failed to get database connection!")
        return None, "fail"

    return engine


# define postgres sqlalchemy engine connection
async def get_engine() -> create_async_engine:
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

    url = "postgresql+asyncpg://{user}:{passwd}@{host}:{port}/{db}".format(
        user=DB_CONFIG["db_user"],
        passwd=DB_CONFIG["db_password"],
        host=DB_CONFIG["db_host"],
        port=DB_CONFIG["db_port"],
        db=DB_CONFIG["db_name"],
    )
    # engine = create_engine(url=url, pool_size=50)
    engine = create_async_engine(url=url, pool_size=50)
    return engine


async def get_session() -> Generator:
    engine = await get_engine()
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
