from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.superuser import Superuser, SuperUserPermissionEnum
from app.application.common.interfaces.uow import UnitOfWork
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


class EnsureSuperuser(CommandHandler):

    def __init__(
        self,
        superuser_repo: repositories.SuperuserRepository,
        uow: UnitOfWork
    ) -> None:
        self.superuser_repo = superuser_repo
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Ensure superuser doesn't exist
        if await self.superuser_repo.check_superuser_exists(
            username=data.username
        ):
            raise superuser_exceptions.SuperuserAlreadyExistsError()
        
        # 2.Create superuser
        superuser = Superuser.create(
            superuser_id=uuid4(), username=data.username, email=data.email,
            password=data.password, permissions=data.permissions,
            created_at=datetime.utcnow()
        )
        await self.superuser_repo.save_superuser(superuser)

        await self.uow.commit()

        return OutputDTO(superuser_id=superuser.id)