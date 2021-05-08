import secrets
from typing import Any, Dict, List, Optional, Union
from pathlib import PurePath

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    PostgresDsn,
    RedisDsn,
    validator,
    EmailStr
)

from fastapi_mail import (
    FastMail,
    ConnectionConfig
)


# pylint: disable=E0213, C0103
class Settings(BaseSettings):
    # important path
    project_dir: PurePath = PurePath(__file__).parent.parent.parent
    media_dir: PurePath = project_dir / "media"
    avatar_height: int = 50
    avatar_width: int = 50

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[Union[AnyHttpUrl, str]] = ['*']

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    REDIS_SERVER: str
    REDIS_USER: Optional[str]
    REDIS_PASSWORD: Optional[str]
    AIOREDIS_URI: Optional[RedisDsn] = None

    @validator("AIOREDIS_URI", pre=True)
    def assemble_redis_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return RedisDsn.build(
            scheme="redis",
            user=values.get("REDIS_USER"),
            password=values.get("REDIS_PASSWORD"),
            host=values.get("REDIS_SERVER")
        )

    MAIL_ENABLE: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: EmailStr
    MAIL_TLS: bool
    MAIL_SSL: bool
    MAIL_AUTHENTICATION_TOKEN_EXPIRE_MINUTES: int = 60

    USERS_OPEN_REGISTRATION: bool = True

    class Config:
        case_sensitive = True


settings = Settings()

if settings.MAIL_ENABLE:
    mail_manager = FastMail(
        ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_TLS=settings.MAIL_TLS,
            MAIL_SSL=settings.MAIL_SSL
        )
    )
