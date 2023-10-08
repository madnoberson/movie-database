from dataclasses import dataclass

from . import dto
from . import exceptions
from . import interfaces


@dataclass(frozen=True, slots=True)
class Login:

    dbr_gateway: interfaces.DatabaseReadingGateway
    password_encoder: interfaces.PasswordEncoder

    async def __call__(self, data: dto.LoginDTO) -> dto.LoginResultDTO:
        # 1.Get query result
        query_result = await self.dbr_gateway.login(username=data.username)
        if query_result is None:
            raise exceptions.UserDoesNotExistError()
        
        # 2.Ensure password is correct
        password_is_correct = await self.password_encoder.verify(
            plain_password=data.password,
            encoded_password=query_result.extra.encoded_password
        )
        if not password_is_correct:
            raise exceptions.UserPasswordIsNotCorrectError()
        
        return dto.LoginResultDTO(query_result.data)