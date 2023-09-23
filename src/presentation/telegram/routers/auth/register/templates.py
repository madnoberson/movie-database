from uuid import UUID


def set_username() -> str:
    return "<b>Username:</b>"


def username_already_exists() -> str:
    return "<b>Username already exists. Enter another one:</b>"


def set_password() -> str:
    return "<b>Password:<b>"


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