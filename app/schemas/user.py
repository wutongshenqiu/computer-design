from typing import Optional
from datetime import datetime
from enum import IntEnum

from pydantic import BaseModel, EmailStr


class Gender(IntEnum):
    MALE = 0
    FEMALE = 1
    UNCLEAR = 2


# Shared properties
class UserBase(BaseModel):
    name: Optional[str] = None
    personal_signature: Optional[str] = None
    gender: Optional[Gender] = None
    birth_date: Optional[datetime] = None
    ancestral_home: Optional[str] = None
    political_status: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None

    is_superuser: Optional[bool] = False
    is_email_activated: Optional[bool] = False
    is_face_activated: Optional[bool] = False

    avatar_path: Optional[str] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
