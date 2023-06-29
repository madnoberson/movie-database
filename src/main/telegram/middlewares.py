from dataclasses import dataclass

from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.presentation.telegram.interactor import TelegramInteractor


@dataclass(frozen=True, slots=True)
class TelegramInteractorMiddleware(BaseMiddleware):

    telegram_interactor: TelegramInteractor

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        data["tg_interactor"] = self.telegram_interactor
        await handler(event, data)