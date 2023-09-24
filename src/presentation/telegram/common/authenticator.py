from abc import ABC, abstractmethod
from uuid import UUID


class Authenticator(ABC):

    @abstractmethod
    async def save_current_user_id(self, user_id: UUID) -> None:
        raise NotImplementedError
    
    @abstractmethod
    async def get_current_user_id(self) -> UUID | None:
        raise NotImplementedError
    
    @abstractmethod
    async def delete_current_user_id(self) -> None:
        raise NotImplementedError