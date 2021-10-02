from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from typing import List, Any

from app.src.models.tag import Tag, TagRead, TagCreate, TagUpdate
from app.src.db.engine import get_session


router = APIRouter()


async def get_tag_or_404(*, session: Session = Depends(get_session),
                      tag_id: int = Path(..., ge=1)):
    try:
        return session.get(Tag, tag_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Tag not found")


@router.get("/", response_model=List[TagRead])
async def read_tags(*, session: Session = Depends(get_session)):
    """
    Get all the existing tags
    """
    tags = session.exec(select(Tag)).all()
    return tags


@router.get("/{tag_id}", response_model=TagRead)
async def read_tag(*, db_tag: Tag = Depends(get_tag_or_404)):
    """
    Get the tag by id
    """
    return db_tag



@router.post("/", response_model=TagRead)
async def create_tags(*, session: Session = Depends(get_session), tag: TagCreate):
    db_t = Tag.from_orm(tag)
    session.add(db_t)
    session.commit()
    session.refresh(db_t)
    return db_t


@router.patch("/{tag_id}", response_model=TagRead)
async def update_tag(*, session: Session = Depends(get_session),
                        db_t: Tag = Depends(get_tag_or_404),
                        t: TagUpdate):
    """
    Modify a tag
    """
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    t_data = t.dict(exclude_unset=True)
    for key, value in t_data.items():
        setattr(db_t, key, value)
    session.add(db_t)
    session.commit()
    session.refresh(db_t)
    return db_t


@router.delete("/{tag_id}")
async def delete_tag(*, session: Session = Depends(get_session),
                     db_tag: Tag = Depends(get_tag_or_404)):
    """
    Delete and remove an existing product type by id; it must be >= 1
    """
    session.delete(db_tag)
    session.commit()
    return {"ok": True}
