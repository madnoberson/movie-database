from abc import abstractmethod
from typing import Protocol
from io import BytesIO


class SupportsSaveMoviePoster(Protocol):

    @abstractmethod
    async def save_movie_poster(self, key: str, poster: BytesIO) -> None:
        raise NotImplementedError


class SupportsUpdateMoviePoster(Protocol):

    @abstractmethod
    async def update_movie_poster(self, key: str, poster: BytesIO) -> None:
        raise NotImplementedError