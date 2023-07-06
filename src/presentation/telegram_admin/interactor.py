from abc import ABC, abstractmethod

from src.application.commands.add_movie.command import AddMovieCommand, AddMovieCommandResult
from src.application.commands.remove_movie.command import RemoveMovieCommand



class TelegramAdminInteractor(ABC):

    @abstractmethod
    def handle_add_movie_command(
        self,
        command: AddMovieCommand
    ) -> AddMovieCommandResult:
        raise NotImplementedError

    @abstractmethod
    def handle_remove_movie_command(
        self,
        command: RemoveMovieCommand
    ) -> None:
        raise NotImplementedError
    