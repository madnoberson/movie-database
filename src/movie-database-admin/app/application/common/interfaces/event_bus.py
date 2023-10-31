from abc import ABC, abstractmethod

from app.domain.events.event import EventT


class EventBus(ABC):

    @abstractmethod
    async def publish(self, event: EventT) -> None:
        raise NotImplementedError