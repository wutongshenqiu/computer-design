from app.schemas import AddressBookCreate
from app.models import User


def prepare_address_book(
    user_me: User,
    user_frident: User
) -> AddressBookCreate:
    return AddressBookCreate(
        user_id=user_me.id,
        friend_id=user_frident.id
    )
