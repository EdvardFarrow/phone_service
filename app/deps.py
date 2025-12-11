import redis.asyncio as redis
from typing import AsyncGenerator
from app.config import settings

pool = redis.ConnectionPool.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
    decode_responses=True
)

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    # The client takes a connection from a ready pool
    client = redis.Redis(connection_pool=pool)
    try:
        yield client
    finally:
        # Close the client (return the connection to the pool), but do NOT close the pool itself
        await client.aclose()