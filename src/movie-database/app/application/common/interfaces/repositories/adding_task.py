from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.adding_task import AddingTask


class AddingTaskRepository(ABC):

    @abstractmethod
    async def check_adding_task_exists(self, kinopoisk_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_adding_task(self, adding_task: AddingTask) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_adding_task(self, adding_task_id: UUID) -> AddingTask | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update_adding_task(self, adding_task: AddingTask) -> None:
        raise NotImplementedError