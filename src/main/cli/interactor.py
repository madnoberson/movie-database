from dataclasses import dataclass

from src.presentation.cli.interactor import CliInteractor
from src.application.common.interfaces.database_gateway import (
    DatabaseGateway
)
from src.application.commands.add_movie.command import (
    AddMovieCommand
)
from src.application.commands.add_movie.handler import (
    AddMovieCommandHandler,
    CommandHandlerResult as AddMovieCommandHandlerResult
)
from src.application.commands.remove_movie.command import (
    RemoveMovieCommand
)
from src.application.commands.remove_movie.handler import (
    RemoveMovieCommandHandler,
    CommandHandlerResult as RemoveMovieCommandHandlerResut
)


@dataclass(frozen=True, slots=True)
class CliInteractorImpl(CliInteractor):

    db_gateway: DatabaseGateway

    def handle_add_movie_command(
        self,
        command: AddMovieCommand
    ) -> AddMovieCommandHandlerResult:
        handler = AddMovieCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)

    def handle_remove_movie_command(
        self,
        command: RemoveMovieCommand
    ) -> RemoveMovieCommandHandlerResut:
        handler = RemoveMovieCommandHandler(
            db_gateway=self.db_gateway
        )
        return handler(command)
