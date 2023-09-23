def set_username() -> str:
    return "<b>Username:</b>"


def set_password() -> str:
    return "<b>Password:</b>"


def confirm(username: str, password: str) -> str:
    return (
        "<b>"
        "You are going to login with following data:\n\n"
        f"Username: {username}\n"
        f"Password: {password}\n\n"
        "Please, confirm."
        "</b>"
    )


def confirmed() -> str:
    return "<b>You have successfully loged in</b>"


def canceled() -> str:
    return "<b>Loging was canceled</b>"