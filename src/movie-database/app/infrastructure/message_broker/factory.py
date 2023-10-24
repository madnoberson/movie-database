from contextlib import asynccontextmanager
from typing import AsyncIterator

from aio_pika.pool import Pool
from aio_pika.abc import AbstractRobustConnection

from .event_bus import EventBusImpl


class EventBusFactory:
    
    def __init__(self, connection_pool: Pool[AbstractRobustConnection]) -> None:
        self.connection_pool = connection_pool

    @asynccontextmanager
    async def build_event_bus(self) -> AsyncIterator[EventBusImpl]:
        async with self.connection_pool.acquire() as connection:
            async with connection.channel() as channel:
                yield EventBusImpl(channel)