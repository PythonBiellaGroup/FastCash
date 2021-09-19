# from sqlmodel import select
from app.src.db.engine import get_db
from sqlmodel import Session, select
from app.src.db.manager import create_table
from app.src.models.db.product import Product
from app.src.models.db.product_type import ProductType
from app.src.models.db.tag import Tag


def test_data():

    # create the tables (come renderle dipendenti da una sessione)
    engine = get_db()
    create_table()

    with Session(engine) as session:
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

        session.add(type_panini)
        session.add(cibo_tag)
        session.add(panino)
        session.add(kebab)

        statement = select(Product)
        results = session.exec(statement)
        products = results.all()
        assert len(products) >= 1

        results = select(Product).where(Product.name == "kebab")
        results = session.exec(statement)
        products = results.all()
        assert len(products) != 0

        session.rollback()
