class UserDoesNotExistError(Exception):
    ...


class UserNotConfirmedError(Exception):
    ...


class UserNotActiveError(Exception):
    ...


class IncorrectPasswordError(Exception):
    ...