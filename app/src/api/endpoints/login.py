from datetime import timedelta
from typing import Any

# from fastapi.security import APIKeyHeader
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.src.config import SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES, API_V1_STR
from app.src.models.token import Token
from app.src.models.app_user import AppUser, AppUserRead
from app.src.db.engine import get_session, get_db, get_session_sqlmodel
from app.src.common.security import (
    get_current_user,
    create_access_token,
    verify_user_by_username,
)

router = APIRouter()

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}/login/access-token")
API_TOKEN = "test"


# Api Token function test
# async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
#     if token != API_TOKEN:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.get("/test")
async def read_items(token: str = Depends(reusable_oauth2)):
    return {"token": token}


@router.post("/access-token", response_model=Token)
def login_access_token(
    db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = verify_user_by_username(
        db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/retrieve-user-by-token", response_model=AppUserRead)
def retrieve_user_by_token(token: str) -> Any:
    """
    Get the user information by the bearer auth token
    """
    current_user = get_current_user(token=token)
    if not current_user:
        raise HTTPException(status_code=400, detail="Token not valid or user not found")
    return current_user


@router.post("/test-token")
def test_token_simple(current_user: AppUser = Depends(get_current_user)) -> Any:
    """
    Test access token
    """
    if current_user:
        return {"user_id": current_user.user_id}
    else:
        return {"user_id": None}
