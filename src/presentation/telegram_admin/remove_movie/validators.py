from uuid import UUID

from .errors import InvalidMovieIdError


def validate_movie_id(text: str | None) -> UUID | None:
    try:
        movie_id = UUID(text)
    except:
        raise InvalidMovieIdError
    
    return movie_id