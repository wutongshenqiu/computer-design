from typing import Generator, AsyncIterator
import asyncio

import pytest

import aioredis
from aioredis import Redis

from app.db.session import SessionLocal
from app.core.config import settings


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()



# TODO
# https://github.com/pytest-dev/pytest-asyncio/issues/171
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def redis() -> AsyncIterator[Redis]:
    client = aioredis.from_url(settings.AIOREDIS_URI)
    yield client

    await client.close()
