from aiogram import Router


def create_add_movie_router() -> Router:
    from .handlers import setup_handlers
    from .error_handlers import setup_error_handlers

    router = Router()
    
    setup_handlers(router)
    setup_error_handlers(router)

    return router