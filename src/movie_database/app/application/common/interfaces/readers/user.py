from abc import ABC, abstractmethod
from uuid import UUID

from app.application.common.query_results import user as query_results


class UserReader(ABC):

    @abstractmethod
    async def get_current_user(self, user_id: UUID) -> query_results.GetCurrentUser | None:
        raise NotImplementedError