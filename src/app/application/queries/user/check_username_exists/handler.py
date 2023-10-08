from dataclasses import dataclass

from . import dto
from . import interfaces


@dataclass(frozen=True, slots=True)
class CheckUsernameExists:

    dbr_gateway: interfaces.DatabaseReadingGateway

    async def __call__(self, data: dto.CheckUsernameExistsDTO) -> dto.CheckUsernameExistsResultDTO:
        query_result = await self.dbr_gateway.check_username_exists(data.username)
        return dto.CheckUsernameExistsResultDTO(query_result.data)