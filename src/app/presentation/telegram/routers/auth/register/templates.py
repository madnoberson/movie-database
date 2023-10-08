from uuid import UUID


def set_username() -> str:
    return "<b>Username:</b>"


def username_is_invalid() -> str:
    return "<b>Username is invalid</b>"


def username_already_exists() -> str:
    return "<b>Username already exists, try another one:</b>"


def set_password() -> str:
    return "<b>Password:</b>"


def password_is_invalid() -> str:
    return "<b>Password is invalid</b>"


def confirm(username: str) -> str:
    return (
        "<b>"
        "You are going to register with following data:\n\n"
        f"Username: {username}\n"
        "Please, confirm."
        "</b>"
    )


def confirmed() -> str:
    return "<b>You have successfully registered</b>"


def canceled() -> str:
    return "<b>Registration was canceled</b>"


def user_already_exists() -> str:
    return "<b>Username already exists, try another one:</b>"