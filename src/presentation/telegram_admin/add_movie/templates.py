from src.domain.models.movie.constants import MovieGenreEnum


def set_title() -> str:
    template = (
        "<b>Title:</b>"
    )
    return template


def set_release_date() -> str:
    template = (
        "<b>Release date:</b>"
    )
    return template


def set_poster() -> str:
    template = (
        "<b>Poster:</b>"
    )
    return template


def set_genres(selected: list[MovieGenreEnum] = []) -> str:
    template = "<b>Genres: {}</b>"
    genres = ", ".join(map(lambda s: s.name.capitalize(), selected))
    formatted_template = template.format(genres)

    return formatted_template


def set_status() -> str:
    template = (
        "<b>Status</b>"
    )
    return template


def set_mpaa() -> str:
    template = (
        "<b>Mpaa:</b>"
    )
    return template


def confirm(**data) -> str:
    template = (
        "<b>Title:</b> {}\n"
        "<b>Release date:</b> {}\n"
        "<b>Genres:</b> {}\n"
        "<b>Status</b> {}\n"
        "<b>Mpaa:</b> {}\n\n"

        "<b>You are going to create movie with this data.\n"
        "Please confirm.</b>"
    )
    formatted_template = template.format(
        data.get("title"),
        data.get("release_date"),
        data.get("genres"),
        data.get("status"),
        data.get("mpaa")
    )

    return formatted_template
    