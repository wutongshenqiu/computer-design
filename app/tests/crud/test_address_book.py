from sqlalchemy.orm import Session

from app.tests.utils import (
    prepare_random_user,
    prepare_many_random_users,
    prepare_address_book
)
from app import crud


def test_create_address_book(db: Session) -> None:
    user1 = crud.user.create(db, obj_in=prepare_random_user())
    user2 = crud.user.create(db, obj_in=prepare_random_user())

    address_book1 = crud.address_book.create(
        db, obj_in=prepare_address_book(user1, user2)
    )
    assert address_book1.user == user1
    assert address_book1.friend == user2

    address_book2 = crud.address_book.create(
        db, obj_in=prepare_address_book(user2, user1)
    )
    assert address_book2.user == user2
    assert address_book2.friend == user1


def test_update_address_book(db: Session) -> None:
    user1 = crud.user.create(db, obj_in=prepare_random_user())
    user2 = crud.user.create(db, obj_in=prepare_random_user())
    user3 = crud.user.create(db, obj_in=prepare_random_user())

    address_book_in = prepare_address_book(user1, user2)
    address_book = crud.address_book.create(db, obj_in=address_book_in)
    assert address_book.user == user1
    assert address_book.friend == user2

    update_address_book_in = address_book_in.copy()
    update_address_book_in.friend_id = user3.id
    update_address_book_in.user_id = user2.id
    update_address_book = crud.address_book.update(
        db, db_obj=address_book, obj_in=update_address_book_in
    )
    assert update_address_book.user == user2
    assert update_address_book.friend == user3


def test_get_address_book(db: Session) -> None:
    user1 = crud.user.create(db, obj_in=prepare_random_user())
    user2 = crud.user.create(db, obj_in=prepare_random_user())

    address_book = crud.address_book.create(
        db, obj_in=prepare_address_book(user1, user2)
    )
    queried_address_book1 = crud.address_book.get_by_user_id(
        db, user_id=user1.id
    )

    assert isinstance(queried_address_book1, list)
    assert len(queried_address_book1) == 1
    assert address_book == queried_address_book1[0]


def test_get_many_address_books(db: Session) -> None:
    user = crud.user.create(db, obj_in=prepare_random_user())
    friends = [
        crud.user.create(db, obj_in=friend) for friend in prepare_many_random_users(50)
    ]

    address_books = [
        crud.address_book.create(
            db, obj_in=prepare_address_book(user, friend)
        )
        for friend in friends
    ]

    assert address_books == crud.address_book.get_by_user_id(
        db, user_id=user.id, limit=50
    )
    assert address_books[:20] == crud.address_book.get_by_user_id(
        db, user_id=user.id
    )
    assert address_books[20:] == crud.address_book.get_by_user_id(
        db, user_id=user.id, offset=20, limit=30
    )
    assert address_books == user.address_books
