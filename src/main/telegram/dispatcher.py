from aiogram import Dispatcher

from src.presentation.telegram.common.error_handlers import setup_error_handlers
from .config import PostgresConfig
from .routes import setup_routes
from .middlewares import setup_middlewares


def create_dipatcher(postgres_config: PostgresConfig) -> Dispatcher:
    dp = Dispatcher()
    
    setup_routes(dp)
    setup_error_handlers(dp)
    setup_middlewares(dp, postgres_config)

    return dp

