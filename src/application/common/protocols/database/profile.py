from typing import Protocol, overload
from abc import abstractmethod
from uuid import UUID

from src.domain.profile import Profile


class SupportsCheckProfileExists(Protocol):

    @overload
    async def check_profile_exists(self, username: str) -> bool:
        raise NotImplementedError
    
    @overload
    async def check_profile_exists(self, profile_id: UUID) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    async def check_profile_exists(
        self, username: str | None = None, profile_id: UUID | None = None
    ) -> bool:
        raise NotImplementedError


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