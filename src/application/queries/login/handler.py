from dataclasses import dataclass

from src.application.common.result import Result
from src.application.common.passoword_encoder import (
    PasswordEncoder
)
from src.domain.models.user.value_objects import (
    Username
)
from .query import LoginQuery, LoginQueryResult
from .interfaces import LoginQueryDBGateway
from .errors import (
    UsernameDoesNotExistError,
    PasswordIsIncorrectError
)


QueryHanlderResult = (
    Result[LoginQueryResult, None] |
    Result[None, UsernameDoesNotExistError] |
    Result[None, PasswordIsIncorrectError]
)


@dataclass(frozen=True, slots=True)
class LoginQueryHandler:

    db_gateway: LoginQueryDBGateway
    password_encoder: PasswordEncoder

    def __call__(self, query: LoginQuery) -> QueryHanlderResult:
        user = self.db_gateway.get_user_by_username(
            username=Username(query.username)
        )
        if user is None:
            error = UsernameDoesNotExistError(query.username)
            return Result(value=None, error=error)
        
        password_is_correct = self.password_encoder.verify(
            password=query.password,
            encoded_password=user.password
        )
        if not password_is_correct:
            error = PasswordIsIncorrectError()
            return Result(value=None, error=error)
        
        query_result = LoginQueryResult(user.id.value)
        result = Result(value=query_result, error=None)

        return result
        
        