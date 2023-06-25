from datetime import datetime, date
from uuid import uuid4

import pytest
from psycopg2._psycopg import connection

from src.infrastructure.psycopg.gateway import (
    PsycopgDatabaseGateway
)
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
from .utils import (
    save_user_to_db,
    save_movie_to_db,
    save_user_movie_rating_to_db,
    get_user_movie_rating_from_db
)


PsycopgConnection = connection


class TestUserMovieRatingProtocolsImplementations:

    @pytest.mark.usefixtures("refresh_database")
    def test_save_user_movie_rating_should_save_user_movie_rating(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        save_user_to_db(
            psycopg_conn=psycopg_conn,
            user=user
        )

        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date.today(),
            rating=0,
            rating_count=0
        )
        save_movie_to_db(
            psycopg_conn=psycopg_conn,
            movie=movie
        )

        user_movie_rating = UserMovieRating(
            user_id=user.id,
            movie_id=movie.id,
            rating=10,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        gateway.save_user_movie_rating(
            user_movie_rating=user_movie_rating
        )
        gateway.commit()

        fetched_user_movie_rating = get_user_movie_rating_from_db(
            psycopg_conn=psycopg_conn,
            user_id=user.id,
            movie_id=movie.id
        )

        assert fetched_user_movie_rating == user_movie_rating
    
    @pytest.mark.usefixtures("refresh_database")
    def test_get_umr_by_user_id_and_movie_id_should_return_umr_when_umr_exists(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        save_user_to_db(
            psycopg_conn=psycopg_conn,
            user=user
        )

        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date.today(),
            rating=0,
            rating_count=0
        )
        save_movie_to_db(
            psycopg_conn=psycopg_conn,
            movie=movie
        )

        user_movie_rating = UserMovieRating(
            user_id=user.id,
            movie_id=movie.id,
            rating=10,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        save_user_movie_rating_to_db(
            psycopg_conn=psycopg_conn,
            user_movie_rating=user_movie_rating
        )

        fetched_umr = gateway.get_user_movie_rating_by_user_id_and_movie_id(
            user_id=user.id,
            movie_id=movie.id
        )

        assert fetched_umr == user_movie_rating
    
    @pytest.mark.usefixtures("refresh_database")
    def test_get_umr_by_user_id_and_movie_id_should_return_none_when_umr_does_not_exist(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        fetched_umr = gateway.get_user_movie_rating_by_user_id_and_movie_id(
            user_id=UserId(uuid4()),
            movie_id=MovieId(uuid4())
        )

        assert fetched_umr is None
    
    @pytest.mark.usefixtures("refresh_database")
    def test_check_umr_existence_should_return_true_when_urm_exists(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        user = User(
            id=UserId(uuid4()),
            username=Username("johndoe"),
            password="encodedpassword",
            created_at=datetime.utcnow()
        )
        save_user_to_db(
            psycopg_conn=psycopg_conn,
            user=user
        )

        movie = Movie(
            id=MovieId(uuid4()),
            title=MovieTitle("There will be blood"),
            release_date=date.today(),
            rating=0,
            rating_count=0
        )
        save_movie_to_db(
            psycopg_conn=psycopg_conn,
            movie=movie
        )

        user_movie_rating = UserMovieRating(
            user_id=user.id,
            movie_id=movie.id,
            rating=10,
            created_at=datetime.utcnow(),
            updated_at=None
        )
        save_user_movie_rating_to_db(
            psycopg_conn=psycopg_conn,
            user_movie_rating=user_movie_rating
        )

        umr_exists = gateway.check_user_movie_rating_existence(
            user_id=user.id,
            movie_id=movie.id
        )

        assert umr_exists
    
    @pytest.mark.usefixtures("refresh_database")
    def test_check_umr_existence_should_return_false_when_urm_does_not_exist(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        umr_exists = gateway.check_user_movie_rating_existence(
            user_id=UserId(uuid4()),
            movie_id=MovieId(uuid4())
        )

        assert not umr_exists
        


    