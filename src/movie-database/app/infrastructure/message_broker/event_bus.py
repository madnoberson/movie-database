from app.domain.events.event import EventT

from aio_pika.abc import AbstractChannel, AbstractTransaction

from app.domain.events.adding_task import AddingTaskEvent
from app.application.common.interfaces.event_bus import EventBus
from .uow import EventBusUnitOfWork
from .mappers import as_message


class EventBusImpl(EventBus):

    EXCHANGE_NAME = "amq.topic"
    ROUTING_KEY_PREFIX = "movie_database"
    ROUTING_KEYS = {
        AddingTaskEvent: "adding_tasks"
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
        return "{}.{}".format(
            self.ROUTING_KEY_PREFIX,
            self.ROUTING_KEYS[type(event).mro()[1]]
        )