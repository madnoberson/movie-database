from app.domain.events.event import EventT

from aio_pika.abc import AbstractChannel

from app.application.common.interfaces.event_bus import EventBus
from .uow import EventBusUnitOfWork


class EventBusImpl(EventBus):

    def __init__(self, channel: AbstractChannel) -> None:
        self.channel = channel

    async def publish(self, event: EventT) -> None:
        ...
    
    async def build_uow(self) -> EventBusUnitOfWork:
        return EventBusUnitOfWork(self.channel.transaction())