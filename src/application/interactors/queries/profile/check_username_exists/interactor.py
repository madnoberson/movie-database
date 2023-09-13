from dataclasses import dataclass

from . import dto
from . import interfaces


@dataclass(frozen=True, slots=True)
class CheckUsernameExists:

    pdb_gateway: interfaces.PresenstationDatabaseGateway

    async def __call__(self, data: dto.CheckUsernameExistsDTO) -> dto.CheckUsernameExistsResultDTO:
        query_result = await self.pdb_gateway.check_username_exists(username=data.username)
        return dto.CheckUsernameExistsResultDTO(query_result.data)