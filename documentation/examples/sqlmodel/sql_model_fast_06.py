# Problema: API per relazioni 1:N: Product
# Create tutte le viste
# https://sqlmodel.tiangolo.com/tutorial/fastapi/teams/
# TO DO - INCOMPLETO
# https://sqlmodel.tiangolo.com/tutorial/fastapi/teams/#add-teams-models
from typing import Optional, List
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, SQLModel, Session, Relationship,\
                     create_engine, select
import uvicorn


# Tabella di associazione n:n tra Tag e Product
class TagProductLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(
        default=None, foreign_key="tag.id", primary_key=True
    )
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.id", primary_key=True
    )


"""
Models di Tag
"""


class TagBase(SQLModel):
    name: str


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    products: List["Product"] =\
        Relationship(back_populates="tags", link_model=TagProductLink)


class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int


# Nel modello update tutti gli attributi devono essere opzionali
class TagUpdate(SQLModel):
    name: Optional[str] = None


"""
Models di ProductType
"""


class ProductTypeBase(SQLModel):
    name: str


class ProductType(ProductTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeRead(ProductTypeBase):
    id: int


# Nel modello update tutti gli attributi devono essere opzionali
class ProductTypeUpdate(SQLModel):
    name: Optional[str] = None


"""
Models di Product
"""


class ProductBase(SQLModel):
    name: str


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    product_type: Optional[int] =\
        Field(default=None, foreign_key="producttype.id")
    tags: Optional[List["Tag"]] =\
        Relationship(back_populates="products", link_model=TagProductLink)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int


class ProductUpdate(SQLModel):
    name: Optional[str] = None


class ProductReadWithTypeAndTags(ProductRead):
    product_type: Optional[ProductTypeRead] = None
    tags: List[TagRead] = []


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/tags/", response_model=TagRead)
def create_tags(*, session: Session = Depends(get_session), tag: TagCreate):
    db_t = Tag.from_orm(tag)
    session.add(db_t)
    session.commit()
    session.refresh(db_t)
    return db_t


@app.post("/product_types/", response_model=ProductTypeRead)
def create_product_type(*, session: Session = Depends(get_session),
                        product_type: ProductTypeCreate):
    db_pt = ProductType.from_orm(product_type)
    session.add(db_pt)
    session.commit()
    session.refresh(db_pt)
    return db_pt


@app.post("/products/", response_model=ProductReadWithTypeAndTags)
def create_product(*, session: Session = Depends(get_session),
                   product: ProductCreate):
    db_p = Product.from_orm(product)
    session.add(db_p)
    session.commit()
    session.refresh(db_p)
    return db_p


# Ora le API docs UI conoscono lo schema
@app.get("/tags/", response_model=List[TagRead])
def read_tags(*, session: Session = Depends(get_session)):
    tags = session.exec(select(Tag)).all()
    return tags


@app.get("/product_types/", response_model=List[ProductTypeRead])
# lte -> less than or equal
def read_product_types(*, session: Session = Depends(get_session),
                       offset: int = 0,
                       limit: int = Query(default=100, lte=100)):
    product_types = session.exec(
        select(ProductType).offset(offset).limit(limit)).all()
    return product_types


@app.get("/product_types/{producttype_id}", response_model=ProductTypeRead)
def read_product_type(*, session: Session = Depends(get_session),
                      producttype_id: int):
    pt = session.get(ProductType, producttype_id)
    if not pt:
        raise HTTPException(
            status_code=404,
            detail="Product type not found"
            )
    return pt


@app.patch("/product_types/{producttype_id}", response_model=ProductTypeRead)
def update_product_type(*, session: Session = Depends(get_session),
                        producttype_id: int, pt: ProductTypeUpdate):
    db_pt = session.get(ProductType, producttype_id)
    if not db_pt:
        raise HTTPException(status_code=404, detail="Product type found")
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    pt_data = pt.dict(exclude_unset=True)
    for key, value in pt_data.items():
        setattr(db_pt, key, value)
    session.add(db_pt)
    session.commit()
    session.refresh(db_pt)
    return db_pt


@app.delete("/product_types/{producttype_id}")
def delete_product_type(*, session: Session = Depends(get_session),
                        producttype_id: int):
    pt = session.get(ProductType, producttype_id)
    if not pt:
        raise HTTPException(
            status_code=404,
            detail="Product type not found"
            )
    session.delete(pt)
    session.commit()
    return {"ok": True}


@app.get("/products/", response_model=List[Product])
# lte -> less than or equal
def read_products(*, session: Session = Depends(get_session),
                  offset: int = 0,
                  limit: int = Query(default=100, lte=100)):
    product_types = session.exec(
        select(Product).offset(offset).limit(limit)).all()
    return product_types


@app.get("/products/{product_id}", response_model=ProductRead)
def read_product(*, session: Session = Depends(get_session),
                 product_id: int):
    p = session.get(Product, product_id)
    if not p:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
            )
    return p


@app.patch("/products/{product_id}", response_model=ProductRead)
def update_product(*, session: Session = Depends(get_session),
                   product_id: int, product: ProductUpdate):
    db_p = session.get(Product, product_id)
    if not db_p:
        raise HTTPException(status_code=404, detail="Product type found")
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    p_data = product.dict(exclude_unset=True)
    for key, value in p_data.items():
        setattr(db_p, key, value)
    session.add(db_p)
    session.commit()
    session.refresh(db_p)
    return db_p


@app.delete("/products/{product_id}")
def delete_product(*, session: Session = Depends(get_session),
                   product_id: int):
    p = session.get(Product, product_id)
    if not p:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
            )
    session.delete(p)
    session.commit()
    return {"ok": True}


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
# In dev, può essere comodo lanciare con
# uvicorn main:app --reload
