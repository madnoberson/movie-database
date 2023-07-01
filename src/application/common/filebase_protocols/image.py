from abc import abstractmethod
from typing import Protocol


class SupportsSaveImage(Protocol):

    @abstractmethod
    def add_image(self):
        raise NotImplementedError
    