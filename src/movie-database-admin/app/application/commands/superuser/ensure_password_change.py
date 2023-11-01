from dataclasses import dataclass
from uuid import UUID

from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import superuser as superuser_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    superuser_id: UUID
    new_password: str


class EnsureSuperuserPasswordChange(CommandHandler):

    def __init__(
        self,
        superuser_repo: repositories.SuperuserRepository,
        uow: UnitOfWork
    ) -> None:
        self.superuser_repo = superuser_repo
        self.uow = uow

    async def __call__(self, data: InputDTO) -> None:
        # 1.Get superuser
        superuser = await self.superuser_repo.get_superuser(
            superuser_id=data.superuser_id
        )
        if superuser is None:
            raise superuser_exceptions.SuperuserDoesNotExistError()

        # 2.Change password
        superuser.change_password(password=data.new_password)
        await self.superuser_repo.update_superuser(superuser)

        await self.uow.commit()
