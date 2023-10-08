from aiogram import Dispatcher

from .routes import setup_routes
from .dependencies import setup_dependencies
from .config import PostgresConfig


async def create_dispatcher(postgres_config: PostgresConfig) -> Dispatcher:
    dispatcher = Dispatcher()

    setup_routes(dispatcher)
    await setup_dependencies(postgres_config, dispatcher)

    return dispatcher