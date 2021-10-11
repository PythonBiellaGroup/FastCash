from fastapi import APIRouter, Depends, HTTPException, Path
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import List
import datetime as dt

from app.src.common.security import get_current_user
from app.src.common.utils import profiling_api
from app.src.models.app_user import AppUser
from app.src.models.tag import Tag, TagRead, TagCreate, TagUpdate
from app.src.db.engine import get_session


router = APIRouter()


async def get_tag_or_404(
    *,
    session: Session = Depends(get_session),
    tag_id: int = Path(..., ge=1),
    current_user: AppUser = Depends(get_current_user),
):
    start_time = dt.datetime.now()
    try:
        db_tag = session.get(Tag, tag_id)
        if db_tag:
            return {
                "db_tag": db_tag,
                "username": current_user.username,
                "start_time": start_time,
            }
        else:
            raise HTTPException(status_code=404, detail="Tag not found")
    except KeyError:
        raise HTTPException(status_code=400, detail="Tag not found")


async def get_tag_by_name_or_404(
    *,
    session: Session = Depends(get_session),
    tag_name: str,
    current_user: AppUser = Depends(get_current_user),
):
    start_time = dt.datetime.now()
    try:
        db_tag = session.exec(select(Tag).where(Tag.name == tag_name)).one()
        if db_tag:
            return {
                "db_tag": db_tag,
                "username": current_user.username,
                "start_time": start_time,
            }
        else:
            raise HTTPException(status_code=404, detail="Tag not found by name")
    except KeyError:
        raise HTTPException(status_code=400, detail="Tag not found by name")


@router.get("/", response_model=List[TagRead])
async def read_tags(
    *,
    session: Session = Depends(get_session),
    current_user: AppUser = Depends(get_current_user),
):
    """
    Get all the existing tags
    """
    start_time = dt.datetime.now()
    tags = session.exec(select(Tag)).all()
    profiling_api("Tags:get:all", start_time, current_user.username)
    return tags


@router.get("/{tag_id}", response_model=TagRead)
async def read_tag(*, tag_id: int, db_tag: Tag = Depends(get_tag_or_404)):
    """
    Get the tag by id
    """
    profiling_api(
        f"Tag:read:by_id:{tag_id}",
        db_tag["start_time"],
        db_tag["username"],
    )
    return db_tag["db_tag"]


@router.post("/", response_model=TagRead)
async def create_tags(
    *,
    session: Session = Depends(get_session),
    tag: TagCreate,
    current_user: AppUser = Depends(get_current_user),
):
    """
    Create a tag
    """
    start_time = dt.datetime.now()
    try:
        db_t = Tag.from_orm(tag)
        session.add(db_t)
        session.commit()
        session.refresh(db_t)
    except IntegrityError:
        raise HTTPException(
            status_code=404, detail="Impossible to create tag with same name"
        )
    profiling_api("Tag:insert:single", start_time, current_user.username)
    return db_t


@router.patch("/{tag_id}", response_model=TagRead)
async def update_tag(
    *,
    tag_id: int,
    session: Session = Depends(get_session),
    tag: TagUpdate,
    db_tag: Tag = Depends(get_tag_or_404),
):
    """
    Modify a tag
    """
    # exclude_unset=True: it would only include the values
    # that were sent by the client
    existing_tag = db_tag["db_tag"]
    tag_data = tag.dict(exclude_unset=True)
    for key, value in tag_data.items():
        setattr(existing_tag, key, value)
    session.add(existing_tag)
    session.commit()
    session.refresh(existing_tag)
    profiling_api(
        f"Tag:update:by_id:{tag_id}",
        db_tag["start_time"],
        db_tag["username"],
    )
    return existing_tag


@router.delete("/{tag_id}")
async def delete_tag(
    *,
    tag_id: int,
    session: Session = Depends(get_session),
    db_tag: Tag = Depends(get_tag_or_404),
):
    """
    Delete and remove an existing product type by id; it must be >= 1
    """
    existing_tag = db_tag["db_tag"]
    session.delete(existing_tag)
    session.commit()
    profiling_api(
        f"Tag:delete:by_id:{tag_id}",
        db_tag["start_time"],
        db_tag["username"],
    )
    return {"ok": True}
