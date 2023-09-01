from typing import Any, Callable
from logging import Logger

from src.application.common.errors.unknown import UnknownError


def handle_unexpected_exceptions(logger: Logger, *exclude: Exception):
    """
    Catches all exceptions raised by `func` except those passed to `exclude`
    and logs them with `logger`
    """
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                if e.__class__ in exclude:
                    raise e
                logger.error(
                    "An unexpected error occured during execution",
                    exc_info=True
                )
                raise UnknownError()
        return wrapper
    return decorator