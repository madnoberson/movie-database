from dataclasses import dataclass

from src.domain.models.user.value_objects import Username


@dataclass(frozen=True, slots=True)
class UsernameAlreadyExistsError(Exception):

    username: Username

