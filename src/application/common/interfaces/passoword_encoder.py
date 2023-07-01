from abc import ABC, abstractmethod


class PasswordEncoder(ABC):

    @abstractmethod
    def encode(self, password: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    def verify(self, password: str, encoded_password: str) -> bool:
        raise NotImplementedError