from typing import TypeVar

from app.application.common.handler import Handler


class QueryHandler(Handler):
    ...


QueryHandlerT = TypeVar("QueryHandlerT", bound=QueryHandler)