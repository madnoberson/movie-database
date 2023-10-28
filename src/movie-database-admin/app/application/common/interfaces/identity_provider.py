from abc import ABC, abstractmethod

from app.domain.models.access_policy import AccessPolicy


class IdentityProvider(ABC):

    @abstractmethod
    async def get_access_policy(self) -> AccessPolicy:
        raise NotImplementedError