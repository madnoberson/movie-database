from abc import ABC, abstractmethod
from typing import IO


class FileRepostory(ABC):

    @abstractmethod
    def add_image(self, image: IO, key: str) -> None:
        raise NotImplementedError
    