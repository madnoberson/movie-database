from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class RemoveMovieCommand:

    movie_id: UUID

    def __post_init__(self) -> None:
        is_valid = (
            isinstance(self.movie_id, UUID)
        )
        if not is_valid:
            raise ValueError()