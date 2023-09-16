from dataclasses import dataclass

from asyncpg import Connection

from src.application.common.interfaces.dbq_gateway import DatabaseQueriesGateway
from src.application.common.query_results import profile as profile_query_results
from src.application.common.query_results import user as user_query_results
from src.infrastructure.application.utils import as_query_result


@dataclass(frozen=True, slots=True)
class AsyncpgDatabaseQueriesGateway(DatabaseQueriesGateway):

    connection: Connection

    async def check_email_exists(self, email: str) -> user_query_results.CheckEmailExists:
        email_exists = await self.connection.fetchval(
            "SELECT 1 FROM users u WHERE u.email = $1 LIMIT 1", email
        )
        return as_query_result(
            user_query_results.CheckEmailExists, {"data": {"email_exists": email_exists}}
        )

    async def check_username_exists(self, username: str) -> profile_query_results.CheckUsernameExists:
        username_exists = await self.connection.fetchval(
            "SELECT 1 FROM profiles p WHERE p.username = $1 LIMIT 1", username
        )
        return as_query_result(
            profile_query_results.CheckUsernameExists, {"data": {"username_exists": username_exists}}
        )