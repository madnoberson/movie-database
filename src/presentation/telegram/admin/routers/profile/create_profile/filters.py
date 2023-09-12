from aiogram.types import Message


def username(message: Message) -> bool:
    return message.text is not None