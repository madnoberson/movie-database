from abc import ABC, abstractmethod

from src.domain.models.user.value_objects import UserId


class ApiAuthenticator(ABC):

    @abstractmethod
    def create_access_token(
        self,
        user_id: UserId
    ) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def create_refresh_token(
        self,
        refresh_token: str
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def validate_access_token(
        self,
        access_token: str
    ):
        raise NotImplementedError