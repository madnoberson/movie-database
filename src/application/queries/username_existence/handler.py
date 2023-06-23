from dataclasses import dataclass

from src.application.common.result import Result
from src.domain.models.user.value_objects import Username
from .query import (
    CheckUsernameExistenceQuery,
    CheckUsernameExistenceQueryResult
)
from .interfaces import UsernameExistenceDBGateway


QueryHandlerResult = (
    Result[CheckUsernameExistenceQueryResult, None]
)


@dataclass(frozen=True, slots=True)
class CheckUsernameExistenceQueryHandler:

    db_gateway: UsernameExistenceDBGateway

    def __call__(
        self,
        query: CheckUsernameExistenceQuery
    ) -> QueryHandlerResult:
        username_exists = self.db_gateway.check_username_existence(
            username=Username(query.username)
        )

        query_result = CheckUsernameExistenceQueryResult(
            exists=username_exists
        )
        result = Result(value=query_result, error=None)

        return result
    