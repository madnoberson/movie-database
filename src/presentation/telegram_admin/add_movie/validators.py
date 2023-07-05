from datetime import date

from aiogram.types.photo_size import PhotoSize

from src.domain.models.movie.constants import (
    MovieStatusEnum,
    MovieGenreEnum,
    MPAAEnum
)
from .errors import (
    InvalidTitleError,
    InvalidReleaseDateError,
    InvalidPosterError,
    InvalidGenresError,
    InvalidStatusError,
    InvalidMpaaError
)


def validate_title(text: str | None) -> str:
    if text is None:
        raise InvalidTitleError()
    
    return text


def validate_release_date(text: str | None) -> date:
    if text is None:
        raise InvalidReleaseDateError()
    if len(raw_release_date := text.split(".")) != 3:
        raise InvalidReleaseDateError()
    try:
        release_date_list = tuple(map(int, raw_release_date))
    except:
        raise InvalidReleaseDateError()
    
    release_date = date(
        year=release_date_list[0],
        month=release_date_list[1],
        day=release_date_list[2]
    )

    return release_date


def validate_poster(photo: list[PhotoSize] | None) -> bytes | None:
    if photo is None:
        ...
    
    return photo[-1].file_id


def validate_genres(text: str | None) -> list[MovieGenreEnum] | None:
    if text is None:
        return None

    raw_genre_list = text.split()

    try:
        genre_list = map(int, raw_genre_list)
        genre_enum_list = map(lambda v: MovieGenreEnum(v), genre_list)
    except ValueError:
        raise InvalidGenresError()
    
    return genre_enum_list


def validate_status(text: str | None) -> MovieStatusEnum | None:
    if text is None:
        return None

    try:
        status = MovieStatusEnum(int(text))
    except:
        raise InvalidStatusError()
    
    return status


def validate_mpaa(text: str | None) -> MPAAEnum | None:
    if text is None:
        return None
    
    try:
        mpaa = MPAAEnum(int(text))
    except:
        raise InvalidMpaaError()
    
    return mpaa