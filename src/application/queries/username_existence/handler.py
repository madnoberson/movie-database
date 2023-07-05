from dataclasses import dataclass

from src.domain.models.user.value_objects import Username
from .query import CheckUsernameExistenceQuery, CheckUsernameExistenceQueryResult
from .interfaces import UsernameExistenceDBGateway


@dataclass(frozen=True, slots=True)
class CheckUsernameExistenceQueryHandler:
    """
    Returns:
        * `CheckUsernameExistenceQueryResult`
    """

    db_gateway: UsernameExistenceDBGateway

    def __call__(
        self,
        query: CheckUsernameExistenceQuery
    ) -> CheckUsernameExistenceQueryResult:
        username_exists = self.db_gateway.check_username_existence(
            username=Username(query.username)
        )
        return CheckUsernameExistenceQueryResult(username_exists)
        
    