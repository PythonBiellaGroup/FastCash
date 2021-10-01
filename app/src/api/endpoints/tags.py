from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.tag import Tag, TagRead, TagCreate, TagUpdate
from app.src.db.engine import get_db
from app.src.db.manager import get_session


router = APIRouter()

@router.get("/", response_model=List[TagRead])
async def read_tags(*, session: Session = Depends(get_session)):
    tags = session.exec(select(Tag)).all()
    return tags


@router.post("/", response_model=TagRead)
async def create_tags(*, session: Session = Depends(get_session), tag: TagCreate):
    db_t = Tag.from_orm(tag)
    session.add(db_t)
    session.commit()
    session.refresh(db_t)
    return db_t

