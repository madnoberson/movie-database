from dataclasses import dataclass
from uuid import UUID

from app.domain.services.access import AccessService
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import superuser as superuser_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    superuser_id: UUID
    new_password: str


class ChangeSuperuserPassword(CommandHandler):

    def __init__(
        self,
        superuser_repo: repositories.SuperuserRepository,
        identity_provider: IdentityProvider,
        access_service: AccessService,
        uow: UnitOfWork
    ) -> None:
        self.superuser_repo = superuser_repo
        self.identity_provider = identity_provider
        self.access_service = access_service
        self.uow = uow

    async def __call__(self, data: InputDTO) -> None:
        # 1.Get current user access policy
        access_policy = await self.identity_provider.get_access_policy()

        # 2.Get superuser
        superuser = await self.superuser_repo.get_superuser(
            superuser_id=data.superuser_id
        )
        if superuser is None:
            raise superuser_exceptions.SuperuserDoesNotExistError()
        
        # 3.Ensure current superuser can change password
        self.access_service.ensure_can_change_superuser_password(
            access_policy=access_policy, superuser=superuser
        )

        # 4.Change password
        superuser.change_password(password=data.new_password)
        await self.superuser_repo.update_superuser(superuser)

        await self.uow.commit()
