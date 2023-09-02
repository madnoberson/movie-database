from src.application.common.errors.user import UserDoesNotExistError, UserNotActiveError


class EmailIsSameAsPreviousError(Exception):
    ...