from typing import Optional

from pydantic import BaseModel


class AddressBookBase(BaseModel):
    user_id: Optional[int] = None
    friend_id: Optional[int] = None


class AddressBookCreate(AddressBookBase):
    user_id: int
    friend_id: int


class AddressBookUpdate(AddressBookBase):
    user_id: int
    friend_id: int


class AddressBookInDBBase(AddressBookBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class AddressBook(AddressBookBase):
    pass


class AddressBookInDB(AddressBookInDBBase):
    pass
