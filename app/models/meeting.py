from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    SMALLINT,
    TIMESTAMP,
    ARRAY
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Meeting(Base):
    id = Column(Integer, primary_key=True, index=True)

    meeting_id = Column(String, nullable=False, index=True)
    meeting_password = Column(String)
    name = Column(String, index=True, nullable=False)
    meeting_tag = Column(String)
    # 0 for security meeting, 1 for normal meeting, 2 for shared meeting
    meeting_type = Column(SMALLINT, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"), index=True)
    participants = Column(ARRAY(Integer))
    designated_participants = Column(ARRAY(Integer))

    creation_time = Column(TIMESTAMP)
    end_time = Column(TIMESTAMP)

    owner = relationship(
        "User", back_populates="meetings", foreign_keys=[owner_id]
    )
