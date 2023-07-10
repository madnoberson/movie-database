from aiogram import Dispatcher

from .config import PostgresConfig, YandexObjectStorageConfig
from .routes import setup_routes
from .middlewares import setup_middlewares


def create_dispatcher(
    postgres_config: PostgresConfig,
    yandex_os_config: YandexObjectStorageConfig
) -> Dispatcher:
    dispatcher = Dispatcher()

    setup_routes(
        dp=dispatcher
    )
    setup_middlewares(
        dp=dispatcher,
        postgres_config=postgres_config,
        yandex_os_config=yandex_os_config
    )

    return dispatcher

