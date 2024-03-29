from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.address_book import AddressBook
from app.schemas.address_book import AddressBookCreate, AddressBookUpdate


class CRUDAddressBook(CRUDBase[AddressBook, AddressBookCreate, AddressBookUpdate]):

    def get_by_user_id(self, db: Session, *,
                       user_id: int,
                       offset: int = 0,
                       limit: int = 20
                       ) -> List[AddressBook]:
        return db.query(AddressBook).filter(
            AddressBook.user_id == user_id
        ).limit(limit).offset(offset).all()

    def get_all_fridend_id(self, db: Session, *,
                           user_id: int,
                           offset: int = 0,
                           limit: int = 20
                           ) -> List[int]:
        return [
            id_ for id_, in
            db.query(AddressBook.friend_id).filter(
                AddressBook.user_id == user_id
            ).limit(limit).offset(offset).all()
        ]

    def check_is_friend(self, db: Session, *,
                        user_id: int,
                        friend_id: int
                        ) -> bool:
        obj = db.query(AddressBook).filter(
            (AddressBook.user_id == user_id) &
            (AddressBook.friend_id == friend_id)
        ).first()

        return obj is not None

    def remove_friend(self, db: Session, *,
                      user_id: int,
                      friend_id: int
                      ) -> Optional[AddressBook]:
        obj = db.query(AddressBook).filter(
            (AddressBook.user_id == user_id) &
            (AddressBook.friend_id == friend_id)
        ).first()

        if obj is None:
            return None

        db.delete(obj)
        db.commit()

        return obj


address_book = CRUDAddressBook(AddressBook)
