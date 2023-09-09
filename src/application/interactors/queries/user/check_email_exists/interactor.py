from dataclasses import dataclass

from . import dto
from . import interfaces


@dataclass(frozen=True, slots=True)
class CheckEmailExists:

    db_gateway: interfaces.DatabaseGateway

    async def __call__(self, data: dto.CheckEmailExistsDTO) -> dto.CheckEmailExistsResultDTO:
        user_exists = await self.db_gateway.check_user_exists(email=data.email)
        return dto.CheckEmailExistsResultDTO(email_exists=user_exists)