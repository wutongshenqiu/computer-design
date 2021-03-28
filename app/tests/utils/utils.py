import random
import string
from datetime import datetime


def random_lower_string(k: int = 32) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=k))


def random_digits_string(k: int = 11) -> str:
    return "".join(random.choices(string.digits, k=k))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_phone_number() -> str:
    return random_digits_string(11)


def random_datetime() -> str:
    return datetime.now()
