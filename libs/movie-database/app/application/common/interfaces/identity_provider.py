from abc import ABC, abstractmethod
from uuid import UUID


class IdentityProvider(ABC):

    @abstractmethod
    async def get_current_user_id(self) -> UUID:
        raise NotImplementedError