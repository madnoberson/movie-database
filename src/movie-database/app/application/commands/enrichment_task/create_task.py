from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from app.domain.models.enrichment_task import EnrichmentTask
from app.domain.events.enrichment_task import EnrichmentTaskCreatedEvent
from app.application.common.interfaces.identity_provider import IdentityProvider
from app.application.common.interfaces.event_bus import EventBus
from app.application.common.interfaces.uow import UnitOfWork
from app.application.common.interfaces import repositories
from app.application.common.exceptions import auth as auth_exceptions
from app.application.common.exceptions import enrichment_task as enrichment_task_exceptions
from app.application.commands.handler import CommandHandler


@dataclass(frozen=True, slots=True)
class InputDTO:

    kinopoisk_id: str


@dataclass(frozen=True, slots=True)
class OutputDTO:

    enrichment_task_id: UUID


class CreateEnrichmentTask(CommandHandler):

    def __init__(
        self,
        enrichment_task_repo: repositories.EnrichmentTaskRepository,
        identity_provider: IdentityProvider,
        event_bus: EventBus,
        uow: UnitOfWork
    ) -> None:
        self.enrichment_task_repo = enrichment_task_repo
        self.identity_provider = identity_provider
        self.event_bus = event_bus
        self.uow = uow
    
    async def __call__(self, data: InputDTO) -> OutputDTO:
        # 1.Get current user id
        current_user_id = await self.identity_provider.get_current_user_id()
        if current_user_id is None:
            raise auth_exceptions.UnauthorizedError()
        
        # 2.Ensure enrichment task doesn't exist
        if await self.enrichment_task_repo.check_enrichment_task_exists(
            kinopoisk_id=data.kinopoisk_id
        ):
            raise enrichment_task_exceptions.EnrichmentTaskAlreadyExistsError()
        
        # 3.Create enrichment task
        enrichment_task = EnrichmentTask.create(
            enrichment_task_id=uuid4(), user_id=current_user_id,
            kinopoisk_id=data.kinopoisk_id, created_at=datetime.utcnow()
        )

        # 4.Save enrichment task
        await self.enrichment_task_repo.save_enrichment_task(enrichment_task)

        # 5.Publish `EnrichmentTaskCreated` event
        event = EnrichmentTaskCreatedEvent(
            id=enrichment_task.id, user_id=enrichment_task.user_id,
            kinopoisk_id=enrichment_task.kinopoisk_id,
            created_at=enrichment_task.created_at
        )
        await self.event_bus.publish(event)

        # 6.Commit changes
        await self.uow.commit()

        return OutputDTO(enrichment_task_id=enrichment_task.id)