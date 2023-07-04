from datetime import date

from aiogram.types.photo_size import PhotoSize

from src.domain.models.movie.constants import (
    MovieStatusEnum,
    MovieGenreEnum,
    MPAAEnum
)


def validate_title(text: str | None) -> str:
    if text is None:
        raise ValueError()


def validate_release_date(text: str | None) -> date:
    if text is None:
        raise ValueError()

    if len(raw_release_date := text.split(".")) != 3:
        raise ValueError()
    
    release_date_list = map(int, raw_release_date)
    
    release_date = date(
        year=release_date_list[0],
        month=release_date_list[1],
        day=release_date_list[2]
    )

    return release_date


def validate_photo(photo: list[PhotoSize] | None):
    ...


def validate_genres(text: str | None) -> list[MovieGenreEnum] | None:
    ...


def validate_status(text: str | None) -> MovieStatusEnum | None:
    ...


def validate_mpaa(text: str | None) -> MPAAEnum | None:
    ...