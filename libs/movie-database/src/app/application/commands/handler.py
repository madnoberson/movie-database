from typing import TypeVar

from app.application.common.handler import Handler


class CommandHandler(Handler):
    ...


CommandHandlerT = TypeVar("CommandHandlerT", bound=CommandHandler)