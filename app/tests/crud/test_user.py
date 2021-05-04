from sqlalchemy.orm import Session

from app import crud
from app.tests.utils import (
    random_email,
    random_lower_string,
    random_datetime,
    random_phone_number,
)
from app.tests.utils import prepare_random_user


def test_create_user(db: Session) -> None:
    email = random_email()
    birth_date = random_datetime()
    phone_number = random_phone_number()
    name = random_lower_string()
    user_in = prepare_random_user(
        name=name,
        birth_date=birth_date,
        phone_number=phone_number,
        email=email
    )

    user = crud.user.create(db, obj_in=user_in)

    assert user.email == email
    assert user.birth_date == birth_date
    assert user.phone_number == phone_number
    assert not user.is_email_activated
    assert not user.is_face_activated
    assert not user.is_superuser
    assert hasattr(user, "hashed_password")


def test_update_user(db: Session) -> None:
    user_in = prepare_random_user()
    user = crud.user.create(db, obj_in=user_in)
    # prevent cache
    prev_hashed_password = user.hashed_password

    update_user_in = user_in.copy()
    update_user_in.birth_date = random_datetime()
    update_user_in.password = random_lower_string()
    update_user = crud.user.update(db, db_obj=user, obj_in=update_user_in)

    assert update_user.email == user.email == user_in.email == update_user_in.email
    assert update_user.birth_date == update_user_in.birth_date != user_in.email
    assert not update_user.is_email_activated
    assert not update_user.is_face_activated
    assert not hasattr(update_user, "password")
    assert hasattr(update_user, "hashed_password")
    assert update_user.hashed_password != prev_hashed_password


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = prepare_random_user(email=email, password=password)

    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(
        db, identifier=email, password=password)
    assert authenticated_user is not None
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(db, identifier=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    user_in = prepare_random_user()
    user = crud.user.create(db, obj_in=user_in)
    assert not crud.user.is_active(user)


def test_check_if_user_is_superuser(db: Session) -> None:
    user_in = prepare_random_user(is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    assert crud.user.is_superuser(user)


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    user_in = prepare_random_user()
    user = crud.user.create(db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_check_if_user_is_active_activated_user(db: Session) -> None:
    user_in = prepare_random_user(
        is_email_activated=True, is_face_activated=True)
    user = crud.user.create(db, obj_in=user_in)

    assert crud.user.is_active(user)
