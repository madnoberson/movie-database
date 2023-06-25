from psycopg2._psycopg import connection

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId, Username
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId, MovieTitle
)
from src.domain.models.user_movie_rating.model import (
    UserMovieRating
)


PsycopgConnection = connection


def save_user_to_db(
    psycopg_conn: PsycopgConnection,
    user: User
) -> None:
    with psycopg_conn.cursor() as cur:
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
    psycopg_conn.commit()


def get_user_by_username_from_db(
    psycopg_conn: PsycopgConnection,
    username: Username
) -> User | None:
    with psycopg_conn.cursor() as cur:
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


def save_movie_to_db(
    psycopg_conn: PsycopgConnection,
    movie: Movie
) -> None:
    with psycopg_conn.cursor() as cur:
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
    psycopg_conn.commit()


def get_movie_by_id_from_db(
    psycopg_conn: PsycopgConnection,
    movie_id: MovieId
) -> Movie | None:
    with psycopg_conn.cursor() as cur:
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


def save_user_movie_rating_to_db(
    psycopg_conn: PsycopgConnection,
    user_movie_rating: UserMovieRating
) -> None:
    with psycopg_conn.cursor() as cur:
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
    psycopg_conn.commit()

def get_user_movie_rating_from_db(
    psycopg_conn: PsycopgConnection,
    user_id: UserId,
    movie_id: MovieId
) -> UserMovieRating:
    with psycopg_conn.cursor() as cur:
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
