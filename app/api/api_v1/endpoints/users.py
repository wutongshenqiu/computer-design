from typing import Any, List, Optional
from pathlib import Path
import mimetypes

from fastapi import (
    APIRouter,
    Body,
    Form,
    UploadFile,
    Depends,
    HTTPException
)
from fastapi.encoders import jsonable_encoder

from pydantic.networks import EmailStr

from sqlalchemy.orm import Session

from PIL import Image

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import remove_file

router = APIRouter()


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)

    return users


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    name: Optional[str] = Form(None),
    personal_signature: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = Depends(deps.check_is_image),
    current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)

    if name is not None:
        user_in.name = name
    if password is not None:
        user_in.password = password
    if personal_signature is not None:
        user_in.personal_signature = personal_signature
    if avatar is not None:
        if current_user.avatar_path:
            remove_file(settings.project_dir / current_user.avatar_path)

        resized_image = Image.open(avatar.file).resize(
            (settings.avatar_width, settings.avatar_height)
        )
        avatar_path = Path(settings.media_dir) / f"{current_user.id}" / \
            f"avatar{mimetypes.guess_extension(avatar.content_type)}"
        if not avatar_path.parent.exists():
            avatar_path.parent.mkdir()
        resized_image.save(avatar_path)
        user_in.avatar_path = str(avatar_path)

    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)

    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/register", response_model=schemas.User)
def create_user_open(
    *,
    db: Session = Depends(deps.get_db),
    name: str = Body(...),
    email: EmailStr = Depends(deps.check_email_exists),
    password: str = Body(...)
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )

    user_in = schemas.UserCreate(
        name=name,
        password=password,
        email=email,
    )
    user = crud.user.create(db, obj_in=user_in)

    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )

    return user
