import json
from dataclasses import asdict
from datetime import datetime
from uuid import UUID

from aio_pika import Message
from aio_pika.abc import AbstractMessage

from app.domain.events.event import EventT


def as_message(event: EventT) -> AbstractMessage:
    data = asdict(event)
    for key, value in data.items():
        if isinstance(value, UUID):
            data[key] = str(value)
        elif isinstance(value, datetime):
            data[key] = value.astimezone().isoformat()
    return Message(body=bytes(json.dumps(data), encoding="utf-8"))
