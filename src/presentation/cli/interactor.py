from abc import ABC, abstractmethod

from src.application.commands.add_movie.command import (
    AddMovieCommand
)
from src.application.commands.add_movie.handler import (
    CommandHandlerResult as AddMovieCommandHandlerResult
)
from src.application.commands.remove_movie.command import (
    RemoveMovieCommand
)
from src.application.commands.remove_movie.handler import (
    CommandHandlerResult as RemoveMovieCommandHandlerResut
)


class CliInteractor(ABC):
    
    @abstractmethod
    def handle_add_movie_command(
        self,
        command: AddMovieCommand
    ) -> AddMovieCommandHandlerResult:
        raise NotImplementedError
    
    @abstractmethod
    def handle_remove_movie_command(
        self,
        command: RemoveMovieCommand
    ) -> RemoveMovieCommandHandlerResut:
        raise NotImplementedError