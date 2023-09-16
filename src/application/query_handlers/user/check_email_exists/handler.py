from dataclasses import dataclass

from . import dto
from . import interfaces


@dataclass(frozen=True, slots=True)
class CheckEmailExists:

    pdb_gateway: interfaces.DatabaseQueriesGateway

    async def __call__(self, data: dto.CheckEmailExistsDTO) -> dto.CheckEmailExistsResultDTO:
        query_result = await self.pdb_gateway.check_email_exists(email=data.email)
        return dto.CheckEmailExistsResultDTO(query_result.data)
