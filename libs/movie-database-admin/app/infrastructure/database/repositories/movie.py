from uuid import UUID

from asyncpg.connection import Connection

from app.domain.models.movie import Movie
from app.application.common.interfaces.repositories import MovieRepository
from app.infrastructure.database.mappers import as_domain_model


class MovieRepositoryImpl(MovieRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    async def save_movie(self, movie: Movie) -> None:
        await self.connection.execute(
            "INSERT INTO movies (id, en_name, created_at) VALUES ($1, $2, $3)",
            movie.id, movie.en_name, movie.created_at
        )
    
    async def get_movie(self, movie_id: UUID) -> Movie | None:
        data = await self.connection.fetchrow(
            "SELECT m.id movie_id, m* FROM movies m WHERE m.id = $1 LIMIT 1",
            movie_id
        )
        return as_domain_model(Movie, data) if data else None

    async def update_movie(self, movie: Movie) -> None:
        await self.connection.execute(
            "UPDATE movies m SET en_name = $1, created_at = $2 WHERE m.id = $3",
            movie.en_name, movie.created_at, movie.id
        )