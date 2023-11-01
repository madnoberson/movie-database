from typing import TypeVar


class Event:
    ...


EventT = TypeVar("EventT", bound=Event)