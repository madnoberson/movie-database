class InvalidTitleError(Exception):

    @property
    def message(self) -> str:
        return "<b>Invalid title</b>"


class InvalidReleaseDateError(Exception):

    @property
    def message(self) -> str:
        return "<b>Invalid release date</b>"


class InvalidPosterError(Exception):
    
    @property
    def message(self) -> None:
        return "<b>Invalid poster</b>"