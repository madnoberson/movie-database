from app.domain.events.event import EventT

from aio_pika.abc import AbstractChannel, AbstractTransaction

from app.domain.events.adding_task import AddingTaskCreatedEvent
from app.application.common.interfaces.event_bus import EventBus
from .uow import EventBusUnitOfWork
from .mappers import as_message


class EventBusImpl(EventBus):

    ROUTING_KEYS = {
        AddingTaskCreatedEvent: "adding_tasks"
    }

    def __init__(
        self,
        channel: AbstractChannel,
        transaction: AbstractTransaction
    ) -> None:
        self.channel = channel
        self.transaction = transaction

    async def publish(self, event: EventT) -> None:
        await self.channel.default_exchange.publish(
            message=as_message(event),
            routing_key=self.ROUTING_KEYS[type(event)]
        )
    
    async def build_uow(self) -> EventBusUnitOfWork:
        return EventBusUnitOfWork(self.transaction)