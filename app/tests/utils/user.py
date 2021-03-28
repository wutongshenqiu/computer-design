from typing import Optional

from app.schemas import UserCreate, Gender

from .utils import (
    random_datetime,
    random_phone_number,
    random_email,
    random_lower_string
)

def prepare_random_user(
    *,
    name: Optional[str] = None,
    gender: Optional[Gender] = None,
    birth_date: Optional[str] = None,
    ancestral_home: Optional[str] = None,
    political_status: Optional[str] = None,
    password: Optional[str] = None,
    email: Optional[str] = None,
    phone_number: Optional[str] = None,
    is_superuser: bool = False,
    is_email_activated: bool = False,
    is_face_activated: bool = False
) -> UserCreate:
    if not name:
        name = random_lower_string()
    if not gender:
        gender = 2
    if not ancestral_home:
        ancestral_home = ""
    if not political_status:
        political_status = ""
    if not birth_date:
        birth_date = random_datetime()
    if not password:
        password = random_lower_string()
    if not phone_number:
        phone_number = random_phone_number()
    if not email:
        email = random_email()

    return UserCreate(
        name=name,
        gender=gender,
        ancestral_home=ancestral_home,
        political_status=political_status,
        birth_date=birth_date,
        password=password,
        email=email,
        phone_number=phone_number,
        is_superuser=is_superuser,
        is_email_activated=is_email_activated,
        is_face_activated=is_face_activated
    )
