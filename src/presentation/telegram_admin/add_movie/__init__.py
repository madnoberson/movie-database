from aiogram import Router


def create_add_movie_router() -> Router:
    from .handlers import setup_handlers

    router = Router()
    
    setup_handlers(router)

    return router