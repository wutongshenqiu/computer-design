from typing import Generator, Optional, AsyncIterator

from fastapi import (
    Depends,
    HTTPException,
    status,
    Body,
    File,
    UploadFile
)
from fastapi.security import OAuth2PasswordBearer

from jose import jwt

from pydantic import ValidationError, EmailStr

from sqlalchemy.orm import Session

import aioredis
from aioredis import Redis

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_redis_db() -> AsyncIterator[Redis]:
    try:
        redis_db = aioredis.from_url(settings.AIOREDIS_URI, decode_responses=True)
        yield redis_db
    finally:
        await redis_db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as errs:
        # https://stefan.sofa-rockers.org/2020/10/28/raise-from/
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from errs

    user = crud.user.get(db, id_=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def check_email_exists(
    db: Session = Depends(get_db), email: EmailStr = Body(...)
) -> EmailStr:
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail={
                "type": "email",
                "msg": "The user with this email already exists in the system"
            }
        )

    return email


def check_phone_number_exists(
    db: Session = Depends(get_db), phone_number: str = Body(...)
) -> str:
    user = crud.user.get_by_phone_number(db, phone_number=phone_number)
    if user:
        raise HTTPException(
            status_code=400,
            detail={
                "type": "phone_number",
                "msg": "The user with this phone number already exists in the system"
            }
        )

    return phone_number


def check_is_image(image: Optional[UploadFile] = File(None)) -> Optional[UploadFile]:
    if image is None:
        return None
    if image.content_type not in {
        "image/gif",
        "image/jpeg",
        "image/png"
    }:
        raise HTTPException(
            status_code=403,
            detail={
                "type": "image",
                "msg": "Only gif, jpg and png are supported"
            }
        )

    return image


async def check_meeting_exists(
    redis_db: Redis = Depends(get_redis_db),
    meeting_id: str = Body(...)
) -> str:
    if await redis_db.hlen(meeting_id) == 0:
        raise HTTPException(
            status_code=403,
            detail={
                "type": "meeting_id",
                "msg": "Meeting doesn't exist"
            }
        )

    return meeting_id
