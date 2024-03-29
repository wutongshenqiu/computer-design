from typing import List, Any, Optional

from fastapi import APIRouter, Depends, Body, HTTPException

from sqlalchemy.orm import Session

from app.api import deps
from app import crud, schemas

router = APIRouter()


@router.post("/me", response_model=List[int])
def read_address_books_me(
    *,
    db: Session = Depends(deps.get_db),
    offset: int = Body(0),
    limit: int = Body(20),
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    return crud.address_book.get_all_fridend_id(
        db=db,
        user_id=current_user.id,
        offset=offset,
        limit=limit
    )


@router.get("/create/{friend_id}", response_model=schemas.AddressBook)
def create_address_book(
    friend_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    if friend_id == current_user.id:
        raise HTTPException(
            status_code=403,
            detail={
                "type": "friend_id",
                "msg": "Can not add yourself as a friend"
            }
        )
    if crud.address_book.check_is_friend(
        db,
        user_id=current_user.id,
        friend_id=friend_id
    ):
        raise HTTPException(
            status_code=403,
            detail={
                "type": "friend_id",
                "msg": f"Already add {friend_id} as a friend"
            }
        )

    address_book_in = schemas.AddressBookCreate(
        user_id=current_user.id,
        friend_id=friend_id
    )
    address_book = crud.address_book.create(db, obj_in=address_book_in)

    return address_book


@router.get("/delete/{friend_id}", response_model=Optional[schemas.AddressBook])
def delete_address_book(
    friend_id: int,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user)
) -> Any:
    return crud.address_book.remove_friend(
        db=db,
        user_id=current_user.id,
        friend_id=friend_id
    )
