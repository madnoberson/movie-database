from uuid import UUID

from asyncpg.connection import Connection

from app.domain.models.movie_rating import MovieRating
from app.application.common.interfaces.repositories import MovieRatingRepository
from app.infrastructure.database.mappers import as_domain_model


class MovieRatingRepositoryImpl(MovieRatingRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection
    
    async def check_movie_rating_exists(
        self, user_id: UUID, movie_id: UUID
    ) -> bool:
        data = await self.connection.fetchval(
            """
            SELECT 1 FROM movie_ratings mr
            WHERE mr.user_id = $1 AND mr.movie_id = $2 LIMIT 1
            """,
            user_id, movie_id
        )
        return bool(data)

    async def save_movie_rating(self, movie_rating: MovieRating) -> None:
        await self.connection.execute(
            """
            INSERT INTO movie_ratings
            (user_id, movie_id, rating, is_full, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            """,
            movie_rating.user_id, movie_rating.movie_id, movie_rating.rating,
            movie_rating.is_full, movie_rating.created_at, movie_rating.updated_at
        )
    
    async def get_movie_rating(
        self, user_id: UUID, movie_id: UUID
    ) -> MovieRating | None:
       data = await self.connection.fetchrow(
           """
           SELECT mr.* FROM movie_ratings mr
           WHERE mr.user_id = $1 AND mr.movie_id = $2 LIMIT 1
           """,
           user_id, movie_id
       )
       return as_domain_model(MovieRating, data) if data else None
    
    async def update_movie_rating(self, movie_rating: MovieRating) -> None:
        await self.connection.execute(
            """
            UPDATE movie_ratings mr SET rating = $1, is_full = $2, updated_at = $3
            WHERE mr.user_id = $4 AND mr.movie_id = $5
            """,
            movie_rating.rating, movie_rating.is_full, movie_rating.updated_at,
            movie_rating.user_id, movie_rating.movie_id
        )
    
    async def delete_movie_rating(self, user_id: UUID, movie_id: UUID) -> None:
        await self.connection.execute(
            """
            DELETE FROM movie_ratings mr WHERE mr.user_id = $1 AND mr.movie_id = $2
            """,
            user_id, movie_id
        )