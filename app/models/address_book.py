from sqlalchemy import (
    Column,
    Integer,
    ForeignKey
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class AddressBook(Base):
    id = Column(Integer, primary_key=True, index=True)
    # TODO
    # (user_id, friend_id) should add unique constrain
    user_id = Column(Integer, ForeignKey("user.id"), index=True)
    friend_id = Column(Integer, ForeignKey("user.id"), index=True)

    user = relationship(
        "User", back_populates="address_books", foreign_keys=[user_id]
    )
    friend = relationship("User", foreign_keys=[friend_id])
