from abc import ABC, abstractmethod

from src.application.common.interfaces import (
    Atomic,
    UserSaver,
    UserReader
)


class RegisterCommandDBGateway(
    Atomic,
    UserSaver,
    UserReader,
    ABC
):
    ...


class PasswordEncoder(ABC):

    @abstractmethod
    def encode(self, password: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def verify(self, encoded_password: str) -> bool:
        raise NotImplementedError