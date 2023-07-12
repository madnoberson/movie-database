from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis

from .config import RedisConfig


def create_storage(config: RedisConfig) -> RedisStorage:
    redis = Redis(
        host=config.host,
        port=config.port,
        db=config.db,
        decode_responses=True
    )

    return RedisStorage(redis)