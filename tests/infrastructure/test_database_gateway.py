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
from src.domain.models.user_movie_rating.model import (
    UserMovieRating
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
    def test_check_user_id_existence_should_return_true_when_user_id_exists(
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

        user_id_exists = gateway.check_user_id_existence(
            user_id=user.id
        )

        assert user_id_exists
    
    @pytest.mark.usefixtures("refresh_database")
    def test_check_user_id_existence_should_return_false_when_user_id_does_not_exist(
        self,
        psycopg_conn: PsycopgConnection
    ):
        gateway = PsycopgDatabaseGateway(psycopg_conn)

        user_id_exists = gateway.check_user_id_existence(
            user_id=UserId(uuid4())
        )

        assert not user_id_exists

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
