from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class SupportsEnqueueFillPersonDataTask(Protocol):

    @abstractmethod
    async def enqueue_fill_person_data_task(self, person_id: UUID) -> None:
        raise NotImplementedError