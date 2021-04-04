from typing import Any
import re

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return '_'.join(map(str.lower, re.findall("[A-Z][^A-Z]*", cls.__name__)))
