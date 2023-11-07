from app.domain.events.event import EventT

from aio_pika.abc import AbstractChannel, AbstractTransaction

from app.domain.events import user as user_events
from app.domain.events import movie_rating as movie_rating_events
from app.application.common.interfaces.event_bus import EventBus
from .uow import EventBusUnitOfWork
from .mappers import as_message


class EventBusImpl(EventBus):

    EXCHANGE_NAME = "movie_database"
    ROUTING_KEYS = {
        user_events.UserCreated: "user.created",
        user_events.UsernameChanged: "user.username_changed",
        movie_rating_events.MovieRated: "movie_rating.created",
        movie_rating_events.MovieRerated: "movie_rating.updated"
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
            routing_key=self.ROUTING_KEYS[type(event)]
        )
    
    def build_uow(self) -> EventBusUnitOfWork:
        return EventBusUnitOfWork(self.transaction)
