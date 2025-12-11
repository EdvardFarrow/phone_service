import pytest
from httpx import AsyncClient, ASGITransport
from fakeredis import aioredis
from app.main import app
from app.deps import get_redis

@pytest.fixture(scope="function")
async def mock_redis():
    # Creating an in-memory Redis instance. decode_responses=True is important to get strings, not bytes.
    redis = aioredis.FakeRedis(decode_responses=True)
    yield redis
    await redis.aclose()

@pytest.fixture(scope="function")
async def client(mock_redis):
    app.dependency_overrides[get_redis] = lambda: mock_redis
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides = {}