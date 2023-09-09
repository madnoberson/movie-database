from dataclasses import dataclass

from . import dto
from . import interfaces


@dataclass(frozen=True, slots=True)
class CheckUsernameExists:

    db_gateway: interfaces.DatabaseGateway

    async def __call__(self, data: dto.CheckUsernameExistsDTO) -> dto.CheckUsernameExistsResultDTO:
        profile_exists = await self.db_gateway.check_profile_exists(username=data.username)
        return dto.CheckUsernameExistsResultDTO(username_exists=profile_exists)