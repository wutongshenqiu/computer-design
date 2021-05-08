from typing import Optional, Union
import asyncio
from pathlib import Path, PurePath

from pydantic import EmailStr

from PIL import Image

from app.core.config import settings


# pylint: disable=import-outside-toplevel
def send_email(
    email_to: EmailStr,
    subject: str,
    body: str,
    subtype: Optional[str] = None
) -> None:
    assert settings.MAIL_ENABLE, "no provided configuration for email variables"
    from app.core.config import mail_manager
    from fastapi_mail import MessageSchema

    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        body=body,
        subtype=subtype
    )

    # TODO
    # ugly, wait async
    asyncio.run(mail_manager.send_message(message))


def send_mail_authentication_email(
    email_to: EmailStr,
    token: str
) -> None:
    # TODO
    # 为了简单这里先不使用 jinja2
    body = f"请点击链接验证邮箱: {settings.SERVER_HOST}{settings.API_V1_STR}/authentication/email/verify/{token}"
    send_email(
        email_to=email_to,
        subject="mail authentication",
        body=body,
    )


def remove_file(path: Union[str, Path, PurePath]) -> None:
    if isinstance(path, (str, PurePath)):
        path = Path(path)
    else:
        raise ValueError("path must be `str` or `PurePath` or `Path`")
    if path.exists(): 
        path.unlink()
