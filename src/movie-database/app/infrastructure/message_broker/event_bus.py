from app.domain.events.event import EventT

from app.application.common.interfaces.event_bus import EventBus
from .uow import EventBusUnitOfWork


class EventBusImpl(EventBus):

    async def publish(self, event: EventT) -> None:
        ...
    
    async def build_uow(self) -> EventBusUnitOfWork:
        return EventBusUnitOfWork()