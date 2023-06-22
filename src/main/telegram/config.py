from dataclasses import dataclass, field
import os


def get_bot_token() -> str | None:
    return os.getenv("bot_token")


@dataclass(frozen=True, slots=True)
class Config:

    bot_token: str = field(
        default_factory=get_bot_token,
        repr=False
    )