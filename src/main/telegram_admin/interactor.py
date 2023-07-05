from dataclasses import dataclass

from src.presentation.telegram_admin.interactor import (
    TelegramAdminInteractor
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
    CommandHandlerResult as RemoveMovieCommandHandlerResult
)
from src.application.common.interfaces.database_gateway import (
    DatabaseGateway
)
from src.application.common.interfaces.filebase_gateway import (
    FilebaseGateway
)


@dataclass(frozen=True, slots=True)
class TelegramAdminInteractorImpl(TelegramAdminInteractor):

    db_gateway: DatabaseGateway
    fb_gateway: FilebaseGateway

    def handle_add_movie_command(
        self,
        command: AddMovieCommand
    ) -> AddMovieCommandHandlerResult:
        handler = AddMovieCommandHandler(
            db_gateway=self.db_gateway,
            fb_gateway=self.fb_gateway
        )
        return handler(command)
    
    def handle_remove_movie_command(
        self,
        command: RemoveMovieCommand
    ) -> RemoveMovieCommandHandlerResult:
        handler = RemoveMovieCommandHandler(
            db_gateway=self.db_gateway,
            fb_gateway=self.fb_gateway
        )
        return handler(command)