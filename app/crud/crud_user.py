from typing import Optional, List

from sqlalchemy.orm.session import Session

from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserInDB, UserSearch
from app.core.security import get_password_hash, verify_password


# pylint: disable=C0103
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_identifier(self, db: Session, *, identifier: str) -> Optional[User]:
        return db.query(User).filter(
            (User.email == identifier) |
            (User.phone_number == identifier) |
            (User.id_card_number == identifier)
        ).first()

    # FIXME
    # elastic search
    def elastic_search(self, db: Session, *,
                       identifier: str) -> List[UserSearch]:
        return [
            UserSearch(*user_info) for user_info in
            db.query(User).with_entities(
                User.name, User.personal_signature, User.is_email_activated
            ).filter(
                (User.name == identifier) |
                (User.phone_number == identifier) |
                (User.email == identifier)
            ).all()
        ]

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def get_by_phone_number(self, db: Session, *, phone_number: str) -> Optional[User]:
        return db.query(User).filter(User.phone_number == phone_number).first()

    def get_by_id_card_number(self, db: Session, *, id_card_number: str) -> Optional[User]:
        return db.query(User).filter(User.id_card_number == id_card_number)

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        obj_in_dict = jsonable_encoder(obj_in)
        obj_in_dict["hashed_password"] = get_password_hash(obj_in.password)
        db_obj = UserInDB(**obj_in_dict)

        return super().create(db, obj_in=db_obj)

    def update(
        self, db: Session, *, db_obj: User, obj_in: UserUpdate
    ) -> User:
        update_data = obj_in.dict(exclude_unset=True)

        if (password := update_data.get("password")):
            update_data["hashed_password"] = get_password_hash(password)
            del update_data["password"]

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, identifier: str, password: str) -> Optional[User]:
        _user = self.get_by_identifier(db, identifier=identifier)
        if not _user:
            return None
        if not verify_password(password, _user.hashed_password):
            return None

        return _user

    def is_active(self, user_: User) -> bool:
        return user_.is_email_activated and user_.is_face_activated

    def is_superuser(self, user_: User) -> bool:
        return user_.is_superuser


user = CRUDUser(User)
