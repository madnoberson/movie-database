from abc import ABC, abstractmethod

from app.application.common.query_results import authentication as query_results


class AuthenticationReader(ABC):

    @abstractmethod
    async def login(self, username: str) -> query_results.Login:
        raise NotImplementedError