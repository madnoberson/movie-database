from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.superuser import Superuser, SuperUserPermissionEnum
from app.domain.services.access import AccessService
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces import repositories
from app.application.common.exceptions import superuser as superuser_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    username: str
    email: str
    password: str
    permissions: list[SuperUserPermissionEnum]


@dataclass(frozen=True, slots=True)
class OutputDTO:

    superuser_id: UUID
    permissions: list[SuperUserPermissionEnum]


class CreateSuperuser(CommandHandler):

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

    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Get current superuser access policy
        access_policy = await self.identity_provider.get_access_policy()

        # 2.Ensure current superuser can create superuser
        self.access_service.ensure_can_create_superuser(access_policy)

        # 3.Ensure superuser doesn't exist
        if await self.superuser_repo.check_superuser_exists(
            username=data.username
        ):
            raise superuser_exceptions.SuperuserAlreadyExistsError()
        
        # 4.Create superuser
        superuser = Superuser.create(
            superuser_id=uuid4(), username=data.username, email=data.email,
            password=data.password, permissions=data.permissions,
            created_at=datetime.utcnow()
        )

        # 5.Save superuser
        await self.superuser_repo.save_superuser(superuser)

        # 6.Commit changes
        await self.uow.commit()

        return OutputDTO(
            superuser_id=superuser.id, permissions=superuser.permissions
        )