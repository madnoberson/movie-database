from asyncpg.connection import Connection

from app.application.common.interfaces.readers import AuthenticationReader
from app.application.common.query_results import authentication as query_resulsts
from app.infrastructure.database.mappers import as_query_result


class AsyncpgAuthenticationReader(AuthenticationReader):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def login(self, username: str) -> query_resulsts.Login | None:
        data = await self.connection.fetchrow(
            """
            SELECT ROW_TO_JSON(u.*) data, ROW_TO_JSON(u.*) extra
            FROM users u WHERE u.username = $1 LIMIT 1
            """,
            username
        )
        if data is None: return None

        data = dict(data)
        data["data"]["user_id"] = data["data"]["id"]
        
        return as_query_result(query_resulsts.Login, data)
