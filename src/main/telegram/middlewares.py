from dataclasses import dataclass

from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.presentation.interactor_factory import InteractorFactory


@dataclass(frozen=True, slots=True)
class IoCMiddleware(BaseMiddleware):

    ioc: InteractorFactory

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        data["ioc"] = self.ioc
        await handler(event, data)