def set_username() -> str:
    """
    Returns message text for
    `register_command_handler_set_username`
    """

    return "<b>Username:</b>"


def username_exists(username: str) -> str:
    """
    Returns message text for
    `register_command_handler_set_username` if username exists
    and for `username_exists_error_handler`
    """

    return f"<b>Username '{username}' exists</b>"


def set_password() -> str:
    """
    Returns message text for
    `register_command_handler_set_password`
    """

    return "<b>Password:</b>"


def successfully_registred() -> str:
    """
    Returns message text for success of
    `register_command_handler_set_password`
    """

    return "<b>Successfully registred</b>"