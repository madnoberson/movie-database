from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.presentation.telegram_admin.interactor import TelegramAdminInteractor


@dataclass(frozen=True, slots=True)
class TelegramInteractorMiddleware(BaseMiddleware):

    interactor: TelegramAdminInteractor

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        data["interactor"] = self.interactor
        await handler(event, data)