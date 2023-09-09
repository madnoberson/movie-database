from dataclasses import dataclass

from . import dto
from . import interfaces


@dataclass(frozen=True, slots=True)
class EnsureEmailExists:

    db_gateway: interfaces.DatabaseGateway

    async def __call__(self, data: dto.EnsureEmailExistsDTO) -> dto.EnsureEmailExistsResultDTO:
        user_exists = await self.db_gateway.ensure_user_exists(email=data.email)
        return dto.EnsureEmailExistsResultDTO(email_exists=user_exists)