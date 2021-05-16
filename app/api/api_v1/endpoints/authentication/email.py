from typing import Any
from datetime import timedelta

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from jose import jwt

from pydantic import ValidationError

from app.api import deps
from app.core import security
from app.core.config import settings
from app import (
    models,
    schemas,
    crud
)
from app.utils import send_mail_authentication_email

router = APIRouter()


@router.get("/create")
def create_mail_authentication_token(
    *,
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    if current_user.is_email_activated:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The email has already been activated"
        )

    verification_code = security.create_access_token(
        subject=current_user.email,
        expires_delta=timedelta(
            minutes=settings.MAIL_AUTHENTICATION_TOKEN_EXPIRE_MINUTES
        )
    )

    send_mail_authentication_email(
        email_to=current_user.email,
        token=verification_code
    )

    return JSONResponse(
        content="email has already been send, please check your mailbox"
    )


# TODO
# for simplcity, we not acquire user
@router.get("/verify/{token}")
def verify_mail_authentication_token(
    *,
    db: Session = Depends(deps.get_db),
    token: str,
    # current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.EmailAuthenticationTokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as errs:
        print(f"token: {token}")
        print(f"secret key: {settings.SECRET_KEY}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate email token",
        ) from errs
    # if token_data.sub != current_user.email:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="email token and user are not compatible"
    #     )

    current_user = crud.user.get_by_email(db, email=token_data.sub)
    user_in = schemas.UserUpdate(**jsonable_encoder(current_user))
    user_in.is_email_activated = True
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)

    return user
