from contextlib import asynccontextmanager
from typing import AsyncIterator

from .event_bus import EventBusImpl


class EventBusFactory:
    
    @asynccontextmanager
    async def build_event_bus(self) -> AsyncIterator[EventBusImpl]:
        yield EventBusImpl()