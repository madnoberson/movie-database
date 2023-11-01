from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.models.superuser import Superuser


class SuperuserRepository(ABC):

    @abstractmethod
    async def check_superuser_exists(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def save_superuser(self, superuser: Superuser) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_superuser(self, superuser_id: UUID) -> Superuser | None:
        raise NotImplementedError
    
    @abstractmethod
    async def update_superuser(self, superuser: Superuser) -> None:
        raise NotImplementedError