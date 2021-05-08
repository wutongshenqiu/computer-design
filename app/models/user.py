from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    SMALLINT,
    TIMESTAMP
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    personal_signature = Column(String)
    # 0 for male, 1 for famale, 2 for not clear?
    gender = Column(SMALLINT)
    birth_date = Column(TIMESTAMP)
    ancestral_home = Column(String)
    political_status = Column(String)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    id_card_number = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    face_img_path = Column(String, unique=True)
    id_card_path = Column(String, unique=True)
    avatar_path = Column(String, unique=True)

    is_email_activated = Column(Boolean(), default=False)
    is_face_activated = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)

    address_books = relationship(
        "AddressBook", back_populates="user", foreign_keys="AddressBook.user_id"
    )

    meetings = relationship(
        "Meeting", back_populates="owner", foreign_keys="Meeting.owner_id"
    )
