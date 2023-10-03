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


def user_does_not_exist() -> str:
    return "<b>User doesn't exist. Make sure the username and password are correct</b>"


def user_password_is_not_correct() -> str:
    return "<b>Password is not correct. Please, try again:</b>"