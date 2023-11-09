from typing import TypeVar


class Policy:
    ...


PolicyT = TypeVar("PolicyT", bound=Policy)