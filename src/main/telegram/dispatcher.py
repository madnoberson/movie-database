from aiogram import Dispatcher

from .config import PostgresConfig, RedisConfig
from .storage import create_storage
from .routes import setup_routes
from .middlewares import setup_middlewares


def create_dipatcher(
    postgres_config: PostgresConfig,
    redis_config: RedisConfig
) -> Dispatcher:
    storage = create_storage(redis_config)
    dp = Dispatcher(storage=storage)
    
    setup_routes(dp)
    setup_middlewares(dp, postgres_config)

    return dp

