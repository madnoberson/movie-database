from uuid import UUID


def set_username() -> str:
    return "<b>Username:</b>"


def username_exists() -> str:
    return "<b>Username already exists</b>"


def confirm(user_id: UUID, username: str) -> str:
    return (
        "<b>"
        "You are going to create profile with following data:\n\n"
        f"User id: {user_id}\n"
        f"Username: {username}\n\n"
        "Please, confirm"
        "</b>"
    )


def confirmed(user_id: UUID, profile_id: UUID, username: str) -> str:
    return (
        "<b>"
        "Profile was successfully created\n\n"
        f"Profile id: {profile_id}\n"
        f"User id: {user_id}\n"
        f"Username: {username}\n"
        "</b>"
    )


def canceled() -> str:
    return "<b>Profile creation was canceled</b>"
