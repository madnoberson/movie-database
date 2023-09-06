from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from src.domain.profile import Profile


class SupportsSaveProfile(Protocol):

    @abstractmethod
    async def save_profile(self, profile: Profile) -> None:
        raise NotImplementedError


class SupportsGetProfile(Protocol):

    @abstractmethod
    async def get_profile(self, profile_id: UUID) -> Profile | None:
        raise NotImplementedError


class SupportsUpdateProfile(Protocol):

    @abstractmethod
    async def update_profile(self, profile: Profile) -> None:
        raise NotImplementedError