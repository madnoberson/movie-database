from dataclasses import dataclass

from asyncpg import Connection

from src.application.common.query_results import user
from src.application.common.interfaces.dbr_gateway import DatabaseReadingGateway
from src.infrastructure.application.utils import as_query_result


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseReadingGateway(DatabaseReadingGateway):

    connection: Connection

    async def check_username_exists(self, username: str) -> user.CheckUsernameExists:
        data = await self.connection.fetchval(
            "SELECT 1 username_exists FROM users u WHERE u.username = $1 LIMIT 1", username
        )
        return as_query_result(user.CheckUsernameExists, data)