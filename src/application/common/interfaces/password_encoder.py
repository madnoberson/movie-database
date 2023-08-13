from abc import ABC, abstractmethod
from typing import final


class PasswordEncoder(ABC):

    @abstractmethod
    def encode(self, password: str) -> str:
        """Returns encoded password"""
        raise NotADirectoryError
    
    @final
    def verify(self, plain_password: str, encoded_password: str) -> bool:
        return self.encode(plain_password) == encoded_password