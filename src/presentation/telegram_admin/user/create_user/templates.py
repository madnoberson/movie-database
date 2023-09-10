from uuid import UUID


def set_email() -> str:
    return "<b>Email:</b>"


def email_exists() -> str:
    return "<b>Email already exists</b>"


def set_password() -> str:
    return "<b>Password:</b>"


def confirm(email: str, password: str) -> str:
    return (
        "<b>"
        "You are going to create user with following data:\n\n"
        f"Email: {email}\n"
        f"Password: {password}\n\n"
        "Please, confirm"
        "</b>"
    )


def confirmed(user_id: UUID, email: str, password: str) -> str:
    return (
        "<b>"
        "User was successfully created\n\n"
        f"User id: {user_id}\n"
        f"Email: {email}\n"
        f"Password: {password}\n"
        "</b>"
    )


def canceled() -> str:
    return "<b>User creation was canceled</b>"