from contextlib import asynccontextmanager
from typing import AsyncIterator

from aio_pika.abc import AbstractRobustConnection

from .event_bus import EventBusImpl


class EventBusFactory:
    
    def __init__(self, connection: AbstractRobustConnection) -> None:
        self.connection = connection

    @asynccontextmanager
    async def build_event_bus(self) -> AsyncIterator[EventBusImpl]:
        async with self.connection.channel(publisher_confirms=False) as channel:
            async with channel.transaction() as transaction:
                yield EventBusImpl(channel, transaction)