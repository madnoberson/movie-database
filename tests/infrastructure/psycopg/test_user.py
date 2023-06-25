from datetime import datetime
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
from .utils import (
    save_user_to_db,
    get_user_by_username_from_db
)


PsycopgConnection = connection


class TestUserProtocolsImplementations:
    
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