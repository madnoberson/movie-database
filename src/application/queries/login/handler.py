from dataclasses import dataclass

from src.application.common.interfaces.passoword_encoder import PasswordEncoder
from src.domain.models.user.value_objects import Username
from .query import LoginQuery, LoginQueryResult
from .interfaces import LoginQueryDBGateway
from .errors import UsernameDoesNotExistError, PasswordIsIncorrectError


@dataclass(frozen=True, slots=True)
class LoginQueryHandler:

    db_gateway: LoginQueryDBGateway
    password_encoder: PasswordEncoder

    def __call__(self, query: LoginQuery) -> LoginQueryResult:
        user = self.db_gateway.get_user_by_username(
            username=Username(query.username)
        )
        if user is None:
            raise UsernameDoesNotExistError(query.username)
        
        password_is_correct = self.password_encoder.verify(
            password=query.password,
            encoded_password=user.password
        )
        if not password_is_correct:
            raise PasswordIsIncorrectError()
                
        return LoginQueryResult(user.id.value)
        
        
        