from dataclasses import dataclass

from psycopg2._psycopg import connection

from src.application.common.database_interfaces.gateway import (
    DatabaseGateway
)
from src.domain.models.user.model import User
from src.domain.models.user.value_objects import (
    UserId, Username
)


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
                """,
                (username.value,)
            )
            username_exists = cur.fetchone()
        
        return username_exists
    
    def commit(self) -> None:
        self.psycopg_conn.commit()
    
    def rollback(self) -> None:
        self.psycopg_conn.rollback()