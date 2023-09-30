from dataclasses import dataclass
from uuid import UUID

from asyncpg import Connection
from asyncpg.transaction import Transaction

from src.domain.user import User
from src.application.common.interfaces.dbw_gateway import DatabaseWritingGateway
from src.infrastructure.application.utils import as_domain_model


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseWritingGateway(DatabaseWritingGateway):

    connection: Connection
    transaction: Transaction

    async def check_user_exists(
        self, username: str | None = None, user_id: UUID | None = None
    ) -> bool:
        c, v = (("u.id", user_id) if user_id else ("u.username", username))
        data = await self.connection.fetchval(f"SELECT 1 FROM users u WHERE {c} = $1", v)
        return bool(data)

    async def save_user(self, user: User) -> None:
        await self.connection.execute(
            """
            INSERT INTO users (id, username, email, encoded_password, created_at)
            VALUES ($1, $2, $3, $4, $5)
            """,
            user.id, user.username, user.email, user.encoded_password, user.created_at
        )
    
    async def get_user(self, user_id: UUID) -> User | None:
        data = await self.connection.fetchrow(
            "SELECT u.* FROM users u WHERE u.id = $1 LIMIT 1", user_id
        )
        return as_domain_model(User, data) if data else None

    async def update_user(self, user: User) -> None:
        await self.connection.execute(
            """
            UPDATE users u
            SET username = $1, email = $2, encoded_password = $3 WHERE u.id = $4
            """,
            user.id
        )

    async def commit(self) -> None:
        await self.transaction.commit()