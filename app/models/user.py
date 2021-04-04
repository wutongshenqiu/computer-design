from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    SMALLINT,
    TIMESTAMP,
)

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    # 0 for male, 1 for famale, 2 for not clear?
    gender = Column(SMALLINT)
    birth_date = Column(TIMESTAMP)
    ancestral_home = Column(String)
    political_status = Column(String)
    phone_number = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    id_card_number = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    face_img_path = Column(String, unique=True)
    id_card_path = Column(String, unique=True)
    avatar_path = Column(String, unique=True)

    is_email_activated = Column(Boolean(), default=False)
    is_face_activated = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)