from datetime import datetime, date
from uuid import uuid4

import pytest
from psycopg2._psycopg import connection

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId, Username
)
from src.domain.models.movie.model import Movie
from src.domain.models.movie.value_objects import (
    MovieId, MovieTitle
)
from src.infrastructure.psycopg.gateway import (
    PsycopgDatabaseGateway
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
    

class TestPsycopgDatabaseGateway:

    @pytest.mark.usefixtures("refresh_database")
    def test_save_user_should_save_user(
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

        gateway.save_user(user)
        gateway.commit()

        fetched_user = get_user_by_username_from_db(
            psycopg_conn=psycopg_conn,
            username=user.username
        )

        assert fetched_user == user
    
    @pytest.mark.usefixtures("refresh_database")
    def test_get_user_by_username_should_return_user(
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

        fetched_user = gateway.get_user_by_username(
            username=user.username
        )

        assert fetched_user == user

    @pytest.mark.usefixtures("refresh_database")
    def test_get_user_by_username_should_return_none_when_user_does_not_exist(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        fetched_user = gateway.get_user_by_username(
            username=Username("nonexistentusername")
        )

        assert fetched_user == None
    
    @pytest.mark.usefixtures("refresh_database")
    def test_check_username_existence_should_return_true_when_username_exists(
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

        username_exists = gateway.check_username_existence(
            username=user.username
        )

        assert username_exists
    
    @pytest.mark.usefixtures("refresh_database")
    def test_check_username_existence_should_return_false_when_username_does_not_exist(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        username_exists = gateway.check_username_existence(
            username=Username("johndoe")
        )

        assert not username_exists
    
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



    