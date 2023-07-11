from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from aiogram import Dispatcher, BaseMiddleware
from aiogram.types import TelegramObject

from src.infrastructure.psycopg.psycopg import get_psycopg2_connection
from src.infrastructure.psycopg.gateway import PsycopgDatabaseGateway
from src.infrastructure.password_encoder import HashlibPasswordEncoder
from src.presentation.telegram.interactor import TelegramInteractor
from .config import PostgresConfig
from .interactor import TelegramInteractorImpl


def setup_middlewares(
    dp: Dispatcher,
    postgres_config: PostgresConfig
) -> None:
    psycopg_conn = get_psycopg2_connection(postgres_config.dsn)
    db_gateway = PsycopgDatabaseGateway(psycopg_conn)
    password_encoder = HashlibPasswordEncoder()

    interactor = TelegramInteractorImpl(
        db_gateway=db_gateway,
        password_encoder=password_encoder
    )
    interactor_middleware = TelegramInteractorMiddleware(interactor)

    dp.message.middleware.register(interactor_middleware)
    dp.callback_query.middleware.register(interactor_middleware)


@dataclass(frozen=True, slots=True)
class TelegramInteractorMiddleware(BaseMiddleware):

    telegram_interactor: TelegramInteractor

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        data["interactor"] = self.telegram_interactor
        await handler(event, data)