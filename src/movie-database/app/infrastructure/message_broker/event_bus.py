from app.domain.events.event import EventT

from aio_pika.abc import AbstractChannel, AbstractTransaction

from app.domain.events import adding_task as adding_task_events
from app.application.common.interfaces.event_bus import EventBus
from .uow import EventBusUnitOfWork
from .mappers import as_message


class EventBusImpl(EventBus):

    EXCHANGE_NAME = "movie_database"
    ROUTING_KEY_PREFIX = "movie_database"
    ROUTING_KEY_ROOTS = {
        adding_task_events.AddingTaskEvent: "adding_tasks"
    }
    ROUTING_KEY_SUFFIXES = {
        adding_task_events.AddingTaskCreatedEvent: "created"
    }

    def __init__(
        self,
        channel: AbstractChannel,
        transaction: AbstractTransaction
    ) -> None:
        self.channel = channel
        self.transaction = transaction

    async def publish(self, event: EventT) -> None:
        exchange = await self.channel.get_exchange(
            name=self.EXCHANGE_NAME
        )
        await exchange.publish(
            message=as_message(event),
            routing_key=self._build_routing_key(event)
        )
    
    def build_uow(self) -> EventBusUnitOfWork:
        return EventBusUnitOfWork(self.transaction)
    
    def _build_routing_key(self, event: EventT) -> str:
        return "{}.{}.{}".format(
            self.ROUTING_KEY_PREFIX,
            self.ROUTING_KEY_ROOTS[type(event).mro()[1]],
            self.ROUTING_KEY_SUFFIXES[type(event)]
        )