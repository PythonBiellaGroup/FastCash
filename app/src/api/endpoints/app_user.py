from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlmodel import Session, select
from typing import List, Any
import datetime as dt


from app.src.models.app_user import (
    AppUser,
    AppUserRead,
    AppUserCreate,
    AppUserUpdate,
)
from app.src.common.security import get_current_admin_user
from app.src.db.engine import get_session
from app.src.common.utils import profiling_api
from app.src.logger import logger

router = APIRouter()


async def get_user_or_404_by_id(
    *,
    session: Session = Depends(get_session),
    user_id: int = Path(..., ge=1),
    current_user: AppUser = Depends(get_current_admin_user),
):
    start_time = dt.datetime.now()
    try:
        if current_user:
            db_user = session.get(AppUser, user_id)
            if db_user:
                return {"db_user": db_user, "start_time": start_time}
            else:
                raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(
                status_code=400, detail="Token not valid or user not authenticated"
            )
    except KeyError:
        raise HTTPException(status_code=400, detail="Product not found")


async def get_user_or_404_by_email(
    *,
    session: Session = Depends(get_session),
    user_email: str = Path(..., ge=1),
    current_user: AppUser = Depends(get_current_admin_user),
):
    start_time = dt.datetime.now()
    try:
        if current_user:
            db_user = session.get(AppUser, user_email)
            if db_user:
                return {"db_user": db_user, "start_time": start_time}
            else:
                raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(
                status_code=400, detail="Token not valid or user not authenticated"
            )
    except KeyError:
        raise HTTPException(status_code=400, detail="Product not found")


async def get_user_or_404_by_username(
    *,
    session: Session = Depends(get_session),
    username: str = Path(..., ge=1),
    current_user: AppUser = Depends(get_current_admin_user),
):
    start_time = dt.datetime.now()
    try:
        if current_user:
            db_user = session.get(AppUser, username)
            if db_user:
                return {"db_user": db_user, "start_time": start_time}
            else:
                raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(
                status_code=400, detail="Token not valid or user not authenticated"
            )
    except KeyError:
        raise HTTPException(status_code=400, detail="Product not found")


@router.get("/", response_model=List[AppUserRead])
async def read_all_users(
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    session: Session = Depends(get_session),
    current_user: AppUser = Depends(get_current_admin_user),
) -> List[AppUser]:
    """
    Retrieve all users (with a limit and offset)
    """
    start_time = dt.datetime.now()
    if not current_user:
        raise HTTPException(
            status_code=400, detail="Token not valid or user not authenticated"
        )
    list_users = session.exec(select(AppUser).offset(offset).limit(limit)).all()
    profiling_api("User:get:all", start_time)
    return list_users


@router.get("/{user_id}", response_model=AppUserRead)
async def read_single_user(
    user_id: int,
    user_time_obj: AppUser = Depends(get_user_or_404_by_id),
) -> AppUser:
    """
    Retrieve a single user by id
    """
    profiling_api(f"User:get:by_id:{user_id}", user_time_obj["start_time"])
    return user_time_obj["db_user"]


@router.post("/", response_model=AppUserRead)
async def create_new_user(
    user: AppUserCreate,
    session: Session = Depends(get_session),
) -> Any:
    """
    Insert new user
    """
    # Check user existing by email and username
    start_time = dt.datetime.now()
    try:
        db_user = AppUser.from_orm(user)
        session.add(db_user)
        session.commit()
        profiling_api("User:insert:single", start_time)
        return db_user
    except Exception as message:
        logger.error(f"Impossible to insert new user: {message}")
        raise HTTPException(
            status_code=400,
            detail="Impossible to insert a new user",
        )


@router.patch("/{user_id}", response_model=AppUserRead)
async def update_user_id(
    user_id: int,
    user: AppUserUpdate,
    session: Session = Depends(get_session),
    user_time_obj: AppUser = Depends(get_user_or_404_by_id),
    current_user: AppUser = Depends(get_current_admin_user),
):
    """
    Update a user by id
    """
    existing_user = user_time_obj["db_user"]
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(existing_user, key, value)
    try:
        session.add(existing_user)
        session.commit()
        session.refresh(existing_user)
        profiling_api(f"User:delete:by_id:{user_id}", user_time_obj["start_time"])
        return existing_user
    except Exception as message:
        logger.error(
            f"Impossible update the user with username: {existing_user.username}, error: {message}"
        )
        logger.exception(message)
        raise HTTPException(
            status_code=400,
            detail=f"Impossible to update the user: {existing_user.username}",
        )


@router.delete("/{user_id}")
async def delete_user_id(
    user_id: int,
    session: Session = Depends(get_current_admin_user),
    user_time_obj: AppUser = Depends(get_user_or_404_by_id),
):
    """Delete a single user by id"""
    existing_user = user_time_obj["db_user"]
    try:
        session.delete(existing_user)
        session.commit()
        profiling_api(f"User:delete:by_id:{user_id}", user_time_obj["start_time"])
        return {"User deleted": True}
    except Exception as message:
        logger.error(f"Impossible to delete the user: {user_id}")
        logger.exception(message)
        raise HTTPException(
            status_code=400,
            detail=f"Impossible to delete the user: {user_id}, {message}",
        )
