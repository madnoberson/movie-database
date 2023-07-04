from aiogram import Router

from .add_movie.handlers import add_movie_router


movies_router = Router()

movies_router.include_router(add_movie_router)