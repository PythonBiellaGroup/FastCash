from os import name
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import List, Any

from app.src.logger import logger
from app.src.models.tag import Tag, TagRead, TagCreate, TagUpdate
from app.src.db.engine import get_session


router = APIRouter()


async def get_tag_or_404(
    *, session: AsyncSession = Depends(get_session), tag_id: int = Path(..., ge=1)
):
    try:
        result = await session.execute(select(Tag).where(Tag.id == tag_id))
        db_tag = result.scalars().first()
        if db_tag:
            logger.info(f"Trovato tag: {db_tag}")
            return db_tag
        else:
            raise HTTPException(status_code=404, detail="Tag not found")
    except KeyError:
        raise HTTPException(status_code=400, detail="Tag not found")


async def get_tag_by_name_or_404(
    *, session: AsyncSession = Depends(get_session), tag_name: str
):
    try:
        result = await session.execute(select(Tag).where(Tag.name == tag_name))
        db_tag = result.scalars().first()
        if db_tag:
            return db_tag
        else:
            raise HTTPException(status_code=404, detail="Tag not found by name")
    except KeyError:
        raise HTTPException(status_code=400, detail="Tag not found by name")



@router.get("/", response_model=List[TagRead])
async def read_tags(*, session: AsyncSession = Depends(get_session)):
    """
    Get all the existing tags
    """
    result = await session.execute(select(Tag))
    tags = result.scalars().all()
    return tags


@router.get("/{tag_id}", response_model=TagRead)
async def read_tag(*, db_tag: Tag = Depends(get_tag_or_404)):
    """
    Get the tag by id
    """
    return db_tag


@router.post("/", response_model=TagRead)
async def create_tags(*, session: AsyncSession = Depends(get_session), tag: TagCreate):
    """
    Create a tag
    """
    try:
        logger.info(tag)
        db_t = Tag(name=tag.name)
        logger.info(db_t)
        #db_t = Tag.from_orm(tag)
        session.add(db_t)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail="Impossible to create tag with same name"
        )
    await session.flush(db_t)
    return db_t


@router.patch("/{tag_id}", response_model=TagRead)
async def update_tag(
    *,
    session: AsyncSession = Depends(get_session),
    db_t: Tag = Depends(get_tag_or_404),
    t: TagUpdate
):
    """
    Modify a tag
    """
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    t_data = t.dict(exclude_unset=True)
    for key, value in t_data.items():
        setattr(db_t, key, value)
    session.add(db_t)
    await session.commit()
    await session.flush(db_t)
    return db_t


@router.delete("/{tag_id}")
async def delete_tag(
    *, session: AsyncSession = Depends(get_session), db_tag: Tag = Depends(get_tag_or_404)
):
    """
    Delete and remove an existing product type by id; it must be >= 1
    """
    await session.delete(db_tag)
    await session.commit()
    await session.flush(db_tag)
    return {"ok": True}
