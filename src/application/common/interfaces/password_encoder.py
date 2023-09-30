from abc import ABC, abstractmethod


class PasswordEncoder(ABC):

    @abstractmethod
    async def encode(self, plain_password: str) -> str:
        raise NotImplementedError
    
    @abstractmethod
    async def verify(self, plain_password: str, encoded_password: str) -> bool:
        raise NotImplementedError