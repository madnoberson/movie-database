from uuid import UUID

from asyncpg.connection import Connection

from app.domain.models.movie import Movie
from app.application.common.interfaces.repositories import MovieRepository
from app.infrastructure.database.mappers import as_domain_model


class MovieRepositoryImpl(MovieRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    async def check_movie_exists(self, movie_id: UUID) -> bool:
        data = await self.connection.fetchval(
            "SELECT 1 FROM movies m WHERE m.id = $1 LIMIT 1", movie_id
        )
        return bool(data)
    
    async def save_movie(self, movie: Movie) -> None:
        await self.connection.execute(
            """
            INSERT INTO movies
            (id, en_name, user_rating_count, user_rating, created_at)
            VALUES ($1, $2, $3, $4, $5)
            """,
            movie.id, movie.en_name, movie.user_rating_count, movie.user_rating,
            movie.created_at
        )
    
    async def get_movie(self, movie_id: UUID) -> Movie | None:
        data = await self.connection.fetchrow(
            "SELECT m.id movie_id, m.* FROM movies m WHERE m.id = $1 LIMIT 1",
            movie_id
        )
        return as_domain_model(Movie, data) if data else None

    async def update_movie(self, movie: Movie) -> None:
        await self.connection.execute(
            """
            UPDATE movies m SET
            en_name = $1, user_rating_count = $2, user_rating = $3 
            WHERE m.id = $4
            """,
            movie.en_name, movie.user_rating_count, movie.user_rating, movie.id
        )