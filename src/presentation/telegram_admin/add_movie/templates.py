from src.domain.models.movie.constants import (
    MovieGenreEnum, MovieStatusEnum
)


def set_title() -> str:
    """
    Returns message text for
    `add_movie_command_set_genres`
    """

    return "<b>Title:</b>"


def set_release_date() -> str:
    """
    Returns message text for
    `add_movie_command_set_release_date`
    """

    return "<b>Release date:</b>"


def set_poster() -> str:
    """
    Returns message text for
    `add_movie_command_set_poster`
    """

    return "<b>Poster:</b>"


def set_genres(selected: list[MovieGenreEnum] = []) -> str:
    """
    Returns message text for 
    `add_movie_command_set_genres`
    """

    template = "<b>Genres: {}</b>"
    genres = ", ".join(map(lambda s: s.name.capitalize(), selected))
    formatted_template = template.format(genres)

    return formatted_template


def set_status() -> str:
    """
    Returns message text for
    `add_movie_command_set_status`
    """

    return "<b>Status</b>"


def set_mpaa() -> str:
    """
    Returns message text for
    `add_movie_command_set_mpaa`
    """

    return "<b>Mpaa:</b>"


def confirm(**data) -> str:
    """
    Returns messsage text for
    `add_movie_command_confirm`
    """

    template = (
        "<b>Title:</b> {}\n"
        "<b>Release date:</b> {}\n"
        "<b>Genres:</b> {}\n"
        "<b>Status</b> {}\n"
        "<b>Mpaa:</b> {}\n\n"

        "<b>You are going to create movie with this data.\n"
        "Please confirm.</b>"
    )

    genre_list = map(
        lambda s: s.name.capitalize(),
        data.get("genres", [])
    )
    status: MovieStatusEnum = data.get("status")

    formatted_template = template.format(
        data.get("title"),
        data.get("release_date"),
        ", ".join(genre_list),
        status.name.capitalize() if status else None,
        data.get("mpaa")
    )

    return formatted_template
    