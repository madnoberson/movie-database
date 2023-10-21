from asyncpg.connection import Connection

from app.domain.models.movie import Movie
from app.application.common.interfaces.repositories import MovieRepository


class MovieRepositoryImpl(MovieRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    async def save_movie(self, movie: Movie) -> None:
        await self.connection.execute(
            "INSERT INTO movies (id, title, created_at) VALUES ($1, $2, $3)",
            movie.id, movie.title, movie.created_at
        )