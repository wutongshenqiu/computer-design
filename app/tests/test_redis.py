import pytest

from aioredis import Redis


@pytest.mark.asyncio
async def test_set_read_key(redis: Redis) -> None:
    await redis.set("hello", "world")
    value = await redis.get("hello")
    assert value.decode() == "world"
