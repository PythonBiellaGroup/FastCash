from sqlmodel import select
from app.src.db.manager import create_table, insert_data, get_session
from app.src.models.db.product import Product
from app.src.models.db.product_type import ProductType
from app.src.models.db.tag import Tag

from app.src.logger import logger
import pytest


@pytest.fixture()
def db_session():
    # get db session
    session = get_session()
    return session


def create_data(db_session):
    logger.debug("Test: creating tables")

    # create the tables (come renderle dipendenti da una sessione)
    create_table()

    # define data
    type_panini = ProductType(name="Panino", description="Tutto ciò che è panino")
    cibo_tag = Tag(name="cibo")
    panino = Product(
        name="panino",
        description="panino buono",
        price=3.30,
        available=True,
        product_type=type_panini,
        tags=[cibo_tag],
    )
    kebab = Product(
        name="kebab",
        description="senza cipolla",
        price=4,
        available=True,
        product_type=type_panini,
        tags=[cibo_tag],
    )

    # create data (definitely)
    # insert_data(type_panini)
    # insert_data(cibo_tag)
    # insert_data(panino)
    # insert_data(kebab)

    db_session.add(type_panini)
    db_session.add(cibo_tag)
    db_session.add(panino)
    db_session.add(kebab)


def test_case(db_session):

    # engine = get_db()
    # with Session(engine) as session:
    statement = select(Product)
    # statement = select(Product).where(Product.name == "Deadpond")
    results = db_session.exec(statement)
    products = results.all()
    assert len(products) >= 1
    results = db_session.select(Product).where(Product.name == "kebab")
    results = db_session.exec(statement)
    products = results.all()
    assert len(products) != 0

    db_session.rollback()

    # my_func_to_delete_user(session, user.id)

    # result = session.query(UserModel).one_or_none()
    # assert result is None


if __name__ == "__main__":

    # create the data
    create_data(db_session)

    test_case(db_session)
