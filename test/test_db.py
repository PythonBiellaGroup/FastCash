from live.src.logger import logger
from sqlmodel import Session, select
from live.src.db.manager import create_table, insert_data
from live.src.db.engine import get_engine
from live.src.models.product import Product
import pytest


@pytest.mark.db
def test_entities_without_rollback():

    # engine creation
    # engine = get_engine()

    # create tables
    create_table()

    panino = Product(
        name="hamburger",
        description="con salse",
        price=4,
        available=True,
        product_type=None,
        tags=None,
    )

    # get session
    # session = get_session()

    # insert data
    insert_data(panino)


def test_entities():

    # engine creation
    engine = get_engine()

    # create tables
    create_table()

    with Session(engine) as session:
        panino = Product(
            name="kebab",
            description="senza cipolla",
            price=3.30,
            available=True,
            product_type=None,
            tags=None,
        )

        session.add(panino)
        logger.debug(f"added panino: {panino}")

        state = select(Product)
        results = session.execute(state)
        products = results.all()

        logger.debug(products)
        assert len(products) >= 1

        session.rollback()


if __name__ == "__main__":
    logger.info("test di esempio")
    # test_entities()
    test_entities_without_rollback()
