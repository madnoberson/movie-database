class InvalidPasswordError(Exception):

    @property
    def message(self) -> str:
        return "<b>Invalid password</b>"


class UserIsNotLogedIn(Exception):

    @property
    def message(self) -> str:
        return "<b>Not logged in</b>"


class UserIsAlreadyLoggedIn(Exception):

    @property
    def message(self) -> str:
        return "<b>Already logged in</b>"