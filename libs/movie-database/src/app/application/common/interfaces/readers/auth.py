from abc import ABC, abstractmethod

from app.application.common.query_results import auth as query_results


class AuthReader(ABC):

    @abstractmethod
    async def login(self, username: str) -> query_results.Login:
        raise NotImplementedError