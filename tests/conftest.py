import pytest
import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection


PsycopgConnection = connection


@pytest.fixture(scope="session")
def psycopg_conn() -> PsycopgConnection:
    test_db_host = "127.0.0.1"
    test_db_port = 5432
    test_db_user = "postgres"
    test_db_password = 1234
    test_db_name = "test_movie_database"

    test_db_dsn = "postgresql://{}:{}@{}:{}/{}".format(
        test_db_user,
        test_db_password,
        test_db_host,
        test_db_port,
        test_db_name
    )

    psycopg2.extras.register_uuid()
    conn = psycopg2.connect(test_db_dsn)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def refresh_database(psycopg_conn: PsycopgConnection) -> None:
    with psycopg_conn.cursor() as cur:
        cur.execute(
            """
            TRUNCATE
                users
            RESTART IDENTITY
            CASCADE
            """
        )
    psycopg_conn.commit()