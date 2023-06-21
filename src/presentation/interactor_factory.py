from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ContextManager

from src.application.commands.register.handler import RegisterCommandHandler


@dataclass(frozen=True, slots=True)
class InteractorFactory(ABC):
    
    @abstractmethod
    def register(self) -> ContextManager[RegisterCommandHandler]:
        raise NotImplementedError

