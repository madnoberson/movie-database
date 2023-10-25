from aio_pika import Message
from aio_pika.abc import AbstractMessage

from app.domain.events.event import EventT


def as_message(event: EventT) -> AbstractMessage:
    return Message(
        body=bytes("Message!", encoding="utf-8")
    )
