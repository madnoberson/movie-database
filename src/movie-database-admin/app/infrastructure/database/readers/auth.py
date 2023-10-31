from asyncpg.connection import Connection

from app.application.common.interfaces.readers import AuthReader
from app.application.common.query_results import auth as query_results
from app.infrastructure.database.mappers import as_query_result


class AuthnReaderImpl(AuthReader):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def login(self, username: str) -> query_results.Login | None:
        data = await self.connection.fetchrow(
            """
            SELECT ROW_TO_JSON(su.*) data, ROW_TO_JSON(su.*) extra
            FROM superusers su WHERE su.username = $1 LIMIT 1
            """,
            username
        )
        if data is None: return None

        data = dict(data)
        data["data"]["superuser_id"] = data["data"]["id"]
        
        return as_query_result(query_results.Login, data)