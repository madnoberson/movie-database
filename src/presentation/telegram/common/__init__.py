from aiogram import Router


def create_common_router() -> Router:
    """
    Returns router with common
    `command/callback_query/error` handlers
    """

    from .handlers import setup_handlers
    from .error_handlers import setup_error_handlers

    router = Router()

    setup_handlers(router)
    setup_error_handlers(router)

    return router