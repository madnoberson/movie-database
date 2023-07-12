def whoami(user_id: str, username: str) -> str:
    """
    Returns message text for `whoami_command_handler`
    """

    template = (
        "<b>User Id:</b> {} \n"
        "<b>Username:</b> {} \n\n"

        "/logout <b>for logout</b>"
    )

    return template.format(user_id, username)


def logout() -> str:
    """
    Returns message text for `logout_command_handler`
    """

    return "<b>You successfully loged out</b>"
