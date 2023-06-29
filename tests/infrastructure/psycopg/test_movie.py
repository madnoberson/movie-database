from datetime import date
from uuid import uuid4

import pytest
from psycopg2._psycopg import connection

from src.infrastructure.psycopg.gateway import (
    PsycopgDatabaseGateway
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId, MovieTitle
)
from .utils import (
    save_movie_to_db,
    get_movie_by_id_from_db
)


PsycopgConnection = connection


class TestsMovieProtocolsImplementations:

    @pytest.mark.usefixtures("refresh_database")
    def test_save_movie_should_save_movie(
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

        gateway.save_movie(movie)
        gateway.commit()

        fetched_movie = get_movie_by_id_from_db(
            psycopg_conn=psycopg_conn,
            movie_id=movie.id
        )

        assert fetched_movie == movie
    
    @pytest.mark.usefixtures("refresh_database")
    def test_update_movie_should_update_movie(
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

        movie.add_rating(10)

        gateway.update_movie(movie)
        gateway.commit()

        fetched_movie = get_movie_by_id_from_db(
            psycopg_conn=psycopg_conn,
            movie_id=movie.id
        )

        assert fetched_movie == movie
    
    @pytest.mark.usefixtures("refresh_database")
    def test_get_movie_by_id_should_return_user(
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

        gateway.save_movie(movie)
        gateway.commit()

        fetched_movie = gateway.get_movie_by_id(
            movie_id=movie.id
        )

        assert fetched_movie == movie
    
    @pytest.mark.usefixtures("refresh_database")
    def test_get_movie_by_id_should_return_none_when_movie_does_not_exist(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        fetched_movie = gateway.get_movie_by_id(
            movie_id=MovieId(uuid4())
        )

        assert not fetched_movie
    
    @pytest.mark.usefixtures("refresh_database")
    def test_check_movie_id_existence_should_return_true_when_movie_id_exists(
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

        movie_id_exists = gateway.check_movie_existence_by_id(
            movie_id=movie.id
        )

        assert movie_id_exists
    
    @pytest.mark.usefixtures("refresh_database")
    def test_check_movie_id_existence_should_return_false_when_movie_id_does_not_exist(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        movie_id_exists = gateway.check_movie_existence_by_id(
            movie_id=MovieId(uuid4())
        )

        assert not movie_id_exists
    
    @pytest.mark.usefixtures("refresh_database")
    def test_remove_movie_by_id_should_remove_movie(
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

        gateway.remove_movie_by_id(movie.id)
        gateway.commit()

        fetched_movie = get_movie_by_id_from_db(
            psycopg_conn=psycopg_conn,
            movie_id=movie.id
        )

        assert fetched_movie == None