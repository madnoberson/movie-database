from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.adding_task import AddingTask, AddingTaskTypeEnum
from app.domain.events.adding_task import AddingTaskCreatedEvent
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import auth as auth_exceptions
from app.application.common.exceptions import adding_task as adding_task_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    kinopoisk_id: str
    adding_type: AddingTaskTypeEnum


@dataclass(frozen=True, slots=True)
class OutputDTO:

    adding_task_id: UUID


class CreateAddingTask(CommandHandler):

    def __init__(
        self,
        adding_task_repo: repositories.AddingTaskRepository,
        identity_provider: IdentityProvider,
        event_bus: EventBus,
        uow: UnitOfWork
    ) -> None:
        self.adding_task_repo = adding_task_repo
        self.identity_provider = identity_provider
        self.event_bus = event_bus
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Get current user id
        current_user_id = await self.identity_provider.get_current_user_id()
        if current_user_id is None:
            raise auth_exceptions.UnauthorizedError()
        
        # 2.Ensure enrichment task doesn't exist
        if await self.adding_task_repo.check_adding_task_exists(
            kinopoisk_id=data.kinopoisk_id
        ):
            raise adding_task_exceptions.AddingTaskAlreadyExistsError()
        
        # 3.Create enrichment task
        adding_task = AddingTask.create(
            adding_task_id=uuid4(), creator_id=current_user_id,
            adding_type=data.adding_type, kinopoisk_id=data.kinopoisk_id,
            created_at=datetime.utcnow()
        )

        # 4.Save enrichment task
        await self.adding_task_repo.save_adding_task(adding_task)

        # 5.Publish `AddingTaskCreated` event
        event = AddingTaskCreatedEvent(
            id=adding_task.id, creator_id=adding_task.creator_id,
            adding_type=adding_task.adding_type,
            kinopoisk_id=adding_task.kinopoisk_id,
            created_at=adding_task.created_at
        )
        await self.event_bus.publish(event)

        # 6.Commit changes
        await self.uow.commit()

        return OutputDTO(adding_task_id=adding_task.id)