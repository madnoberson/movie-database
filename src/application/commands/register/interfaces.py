from abc import ABC, abstractmethod
from typing import Protocol

from src.application.common.database_intefaces.user import (
    SupportsSaveUser,
    SupportsGetUserByUsername
)
from src.application.common.database_intefaces.atomic import (
    SupportsAtomic
)


class RegisterCommandDBGateway(
    SupportsAtomic,
    SupportsSaveUser,
    SupportsGetUserByUsername,
    Protocol
):
    ...


class PasswordEncoder(ABC):

    @abstractmethod
    def encode(self, password: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def verify(self, password: str, encoded_password: str) -> bool:
        raise NotImplementedError