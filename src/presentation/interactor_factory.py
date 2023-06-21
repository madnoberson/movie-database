from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ContextManager

from src.application.commands.register.handler import RegisterCommandHandler
from src.application.queries.login.handler import LoginQueryHandler


@dataclass(frozen=True, slots=True)
class InteractorFactory(ABC):
    
    @abstractmethod
    def register(self) -> ContextManager[RegisterCommandHandler]:
        raise NotImplementedError

    @abstractmethod
    def login(self) -> ContextManager[LoginQueryHandler]:
        raise NotImplementedError

