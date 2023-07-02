from datetime import date
from uuid import uuid4

import pytest
from psycopg2._psycopg import connection

from src.infrastructure.psycopg.gateway import (
    PsycopgDatabaseGateway
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId,
    MovieTitle,
    MoviePosterKey
)
from src.domain.models.movie.constants import (
    MovieStatusEnum,
    MPAAEnum
)
from src.domain.models.movie_genres.model import MovieGenres
from src.domain.models.movie_genres.constants import MovieGenreEnum
from .utils import save_movie_to_db


PsycopgConnection = connection


def get_movie_genres_from_db(
    psycopg_conn: PsycopgConnection,
    movie_id: MovieId
) -> MovieGenres | None:
    with psycopg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                movies_genres.genre_id
            FROM
                movies_genres
            WHERE
                movies_genres.movie_id = %s
            """,
            (movie_id.value,)
        )
        genres_data = cur.fetchall()
    
    if not genres_data:
        return None
    
    return MovieGenres(
        movie_id=movie_id,
        genres=[
            MovieGenreEnum(genre_data[0])
            for genre_data in genres_data
        ]
    )


class TestMovieGenres:

    @pytest.mark.usefixtures("refresh_database")
    def test_save_movie_genres_should_save_movie_genres(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date(2008, 2, 28),
            rating=0,
            rating_count=0
        )
        save_movie_to_db(
            psycopg_conn=psycopg_conn,
            movie=movie
        )

        movie_genres = MovieGenres(
            movie_id=movie.id,
            genres=[MovieGenreEnum(1), MovieGenreEnum(6)]
        )
        gateway.save_movie_genres(movie_genres)

        fetched_movie_genres = get_movie_genres_from_db(
            psycopg_conn=psycopg_conn,
            movie_id=movie.id
        )

        assert fetched_movie_genres == movie_genres

