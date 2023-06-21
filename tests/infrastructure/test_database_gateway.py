from datetime import datetime
from uuid import uuid4

import pytest
from psycopg2._psycopg import connection

from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId, Username
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
) -> User:
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
    
    