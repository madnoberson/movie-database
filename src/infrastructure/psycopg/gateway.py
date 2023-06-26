from dataclasses import dataclass

from psycopg2._psycopg import connection

from src.application.common.database_interfaces.gateway import (
    DatabaseGateway
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId, MovieTitle
)
from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId, Username
)
from src.domain.models.user_movie_rating.model import UserMovieRating


PsycopgConnection = connection


@dataclass(frozen=True, slots=True)
class PsycopgDatabaseGateway(DatabaseGateway):

    psycopg_conn: PsycopgConnection
    
    def save_user(self, user: User) -> None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users
                (
                    id,
                    username,
                    encoded_password,
                    created_at
                )
                VALUES
                (%s, %s, %s, %s)
                """,
                (
                    user.id.value,
                    user.username.value,
                    user.password,
                    user.created_at
                )
            )
    
    def get_user_by_username(
        self,
        username: Username
    ) -> User | None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    users.id,
                    users.username,
                    users.encoded_password,
                    users.created_at
                FROM
                    users
                WHERE
                    users.username = %s
                LIMIT 1
                """,
                (username.value,)
            )
            user_data = cur.fetchone()

        if not user_data:
            return None

        return User(
            id=UserId(user_data[0]),
            username=Username(user_data[1]),
            password=user_data[2],
            created_at=user_data[3]
        )
    
    def get_user_by_id(
        self,
        user_id: UserId
    ) -> User | None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    users.id,
                    users.username,
                    users.encoded_password,
                    users.created_at
                FROM
                    users
                WHERE
                    users.id = %s
                LIMIT 1
                """,
                (user_id.value,)
            )
            user_data = cur.fetchone()

        if not user_data:
            return None

        return User(
            id=UserId(user_data[0]),
            username=Username(user_data[1]),
            password=user_data[2],
            created_at=user_data[3]
        )

    def check_user_id_existence(
        self,
        user_id: UserId
    ) -> bool:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1
                FROM users
                WHERE users.id = %s
                LIMIT 1
                """,
                (user_id.value,)
            )
            user_id_exists = cur.fetchone()
        
        return not user_id_exists is None
    
    def check_username_existence(
        self,
        username: Username
    ) -> bool:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1
                FROM users
                WHERE users.username = %s
                LIMIT 1
                """,
                (username.value,)
            )
            username_exists = cur.fetchone()
        
        return not username_exists is None
    
    def save_movie(self, movie: Movie) -> None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO movies
                (
                    id,
                    title,
                    release_date,
                    rating, 
                    rating_count
                )
                VALUES
                (
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    movie.id.value,
                    movie.title.value,
                    movie.release_date,
                    movie.rating,
                    movie.rating_count
                )
            )

    def get_movie_by_id(
        self,
        movie_id: MovieId
    ) -> Movie | None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    movies.id,
                    movies.title,
                    movies.release_date,
                    movies.rating,
                    movies.rating_count
                FROM
                    movies
                WHERE
                    movies.id = %s
                LIMIT 1
                """,
                (movie_id.value,)
            )
            movie_data = cur.fetchone()
        
        if not movie_data:
            return None
        
        return Movie(
            id=MovieId(movie_data[0]),
            title=MovieTitle(movie_data[1]),
            release_date=movie_data[2],
            rating=movie_data[3],
            rating_count=movie_data[4]
        )
    
    def update_movie(self, movie: Movie) -> None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                UPDATE
                    movies
                SET
                    title = %s,
                    release_date = %s,
                    rating = %s,
                    rating_count = %s
                WHERE
                    movies.id = %s
                """,
                (
                    movie.title.value,
                    movie.release_date,
                    movie.rating,
                    movie.rating_count,
                    movie.id.value
                )
            )

    def save_user_movie_rating(
        self,
        user_movie_rating: UserMovieRating
    ) -> None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO user_movie_ratings
                (
                    user_id,
                    movie_id,
                    rating,
                    created_at,
                    updated_at
                )
                VALUES
                (
                    %s, %s, %s, %s, %s
                )
                """,
                (
                    user_movie_rating.user_id.value,
                    user_movie_rating.movie_id.value,
                    user_movie_rating.rating,
                    user_movie_rating.created_at,
                    user_movie_rating.updated_at
                )
            )
    
    def update_user_movie_rating(
        self,
        user_movie_rating: UserMovieRating
    ) -> None:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                UPDATE
                    user_movie_ratings
                SET
                    rating = %s,
                    updated_at = %s
                WHERE
                    user_movie_ratings.user_id = %s
                AND
                    user_movie_ratings.movie_id = %s
                """,
                (
                    user_movie_rating.rating,
                    user_movie_rating.updated_at,
                    user_movie_rating.user_id.value,
                    user_movie_rating.movie_id.value
                )
            )

    def get_user_movie_rating_by_user_id_and_movie_id(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> UserMovieRating:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    user_movie_ratings.user_id,
                    user_movie_ratings.movie_id,
                    user_movie_ratings.rating,
                    user_movie_ratings.created_at,
                    user_movie_ratings.updated_at
                FROM
                    user_movie_ratings
                WHERE
                    user_movie_ratings.user_id = %s
                AND
                    user_movie_ratings.movie_id = %s
                LIMIT 1
                """,
                (
                    user_id.value,
                    movie_id.value
                )
            )
            user_movie_rating_data = cur.fetchone()
        
        if not user_movie_rating_data:
            return None

        return UserMovieRating(
            user_id=UserId(user_movie_rating_data[0]),
            movie_id=MovieId(user_movie_rating_data[1]),
            rating=user_movie_rating_data[2],
            created_at=user_movie_rating_data[3],
            updated_at=user_movie_rating_data[4]
        )
    
    def check_user_movie_rating_existence(
        self,
        user_id: UserId,
        movie_id: MovieId
    ) -> bool:
        with self.psycopg_conn.cursor() as cur:
            cur.execute(
                """
                SELECT 1
                FROM
                    user_movie_ratings
                WHERE
                    user_movie_ratings.user_id = %s
                AND
                    user_movie_ratings.movie_id = %s
                LIMIT 1
                """,
                (
                    user_id.value,
                    movie_id.value
                )
            )
            user_movie_rating_exists = cur.fetchone()
        
        return not user_movie_rating_exists is None
    
    def commit(self) -> None:
        self.psycopg_conn.commit()
    
    def rollback(self) -> None:
        self.psycopg_conn.rollback()