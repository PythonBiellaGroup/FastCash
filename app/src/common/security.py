# from datetime import datetime, timedelta
# from pathlib import Path
# from typing import Any, Dict, Optional

# import emails
# from emails.template import JinjaTemplate
from jose import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from typing import Any, Optional, Union
from passlib.context import CryptContext

from app.src.db.manager import get_db
from app.src.models.app_user import AppUser
from app.src.models.token import TokenPayload

from app.src.config import (
    API_V1_STR,
    SECURITY_ALGORITHM,
    SECURITY_SECRET_KEY,
    SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES,
)


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{API_V1_STR}/login/access-token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_current_user(*, token: str = Depends(reusable_oauth2)) -> AppUser:
    try:
        payload = jwt.decode(
            token, SECURITY_SECRET_KEY, algorithms=[SECURITY_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user_id = token_data.sub
    engine = get_db()
    with Session(engine) as session:
        user = session.get(AppUser, user_id)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found or not authenticated"
        )
    return user


def get_current_admin_user(
    current_user: AppUser = Depends(get_current_user),
) -> bool:
    if not current_user.isAdmin:
        raise HTTPException(status_code=400, detail="User is not admin or don't exist")
    if current_user:
        return True
    else:
        return False


def test_user(current_user: AppUser = Depends(get_current_user)) -> bool:
    """
    Test access token
    """
    if current_user:
        return True
    else:
        return False


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, SECURITY_SECRET_KEY, algorithm=SECURITY_ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_user_by_username(
    db: Session, *, username: str, password: str
) -> Optional[AppUser]:
    user = db.query(AppUser).filter(AppUser.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.token):
        return None
    return user


def verify_user_by_email(
    db: Session, *, email: str, password: str
) -> Optional[AppUser]:
    user = db.query(AppUser).filter(AppUser.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.token):
        return None
    return user


# def verify_password_reset_token(token: str) -> Optional[str]:
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         return decoded_token["email"]
#     except jwt.JWTError:
#         return None


# possibility to check if an user is active or not
# def get_current_active_user(
#     current_user: ShinyUser = Depends(get_current_user),
# ) -> ShinyUser:
#     if not current_user.isActive:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
