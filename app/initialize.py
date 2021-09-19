# Initialize the db with the tables and dummy data
from app.src.logger import logger
from app.src.db.manager import create_table, insert_data
from app.src.models.db.product import Product
from app.src.models.db.product_type import ProductType
from app.src.models.db.tag import Tag


def create_data():
    logger.debug("Initialization - Creating tables")

    # create the tables
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

    # create data
    insert_data(type_panini)
    insert_data(cibo_tag)
    insert_data(panino)
    insert_data(kebab)

    # refresh_data(cibo_tag)


if __name__ == "__main__":
    logger.info("Initialization of DB for the first run")
    create_data()
    logger.info("Initialization completed")
