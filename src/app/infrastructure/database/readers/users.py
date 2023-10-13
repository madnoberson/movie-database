from uuid import UUID

from asyncpg.connection import Connection

from app.application.common.interfaces.readers import UserReader
from app.application.common.query_results import user as query_results
from app.infrastructure.database.mappers import as_query_result


class AsyncpgUsersReader(UserReader):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def get_current_user(self, user_id: UUID) -> query_results.GetUser | None:
        data = await self.connection.fetchrow(
            "SELECT ROW_TO_JSON(u.*) data FROM users u WHERE u.id = $1 LIMIT 1", user_id
        )
        return as_query_result(query_results.GetUser, data)