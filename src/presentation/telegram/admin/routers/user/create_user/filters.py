from aiogram.types import Message


def email(message: Message) -> bool:
    return message.text is not None


def password(message: Message) -> bool:
    return message.text is not None