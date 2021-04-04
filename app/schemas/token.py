from typing import Optional

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    

class EmailAuthenticationTokenPayload(BaseModel):
    sub: Optional[EmailStr] = None
