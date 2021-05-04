from typing import Optional, List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.address_book import AddressBook
from app.schemas.address_book import AddressBookCreate, AddressBookUpdate


class CRUDAddressBook(CRUDBase[AddressBook, AddressBookCreate, AddressBookUpdate]):

    def get_by_user_id(self, db: Session, *,
                       user_id: int,
                       offset: int = 0,
                       limit: int = 20
                       ) -> Optional[List[AddressBook]]:
        return db.query(AddressBook).filter(
            AddressBook.user_id == user_id
        ).limit(limit).offset(offset).all()


address_book = CRUDAddressBook(AddressBook)
