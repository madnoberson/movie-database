from dataclasses import dataclass, field
from uuid import UUID

from src.domain.user import User
from src.domain.profile import Profile
from src.application.common.interfaces.database_gateway import DatabaseGateway


@dataclass(frozen=True, slots=True)
class InMemoryDatabaseGateway(DatabaseGateway):

    users: list[User] = field(init=False, default_factory=set)
    profiles: list[Profile] = field(init=False, default_factory=set)

    async def ensure_user_does_not_exist(self, email: str) -> bool:
        for user in self.users:
            if user.email != email:
                continue
            return True
        return False

    async def save_user(self, user: User) -> None:
        self.users.append(user)
    
    async def get_user(self, user_id: UUID) -> User | None:
        for user in self.users:
            if user.id != user_id:
                continue
            return user
    
    async def update_user(self, user: User) -> None:
        for user in self.users:
            if user.id != user.id:
                continue
            self.users.remove(user)
            self.users.append(user)
            break
    
    async def save_profile(self, profile: Profile) -> None:
        self.profiles.append(profile)
    
    async def get_profile(self, profile_id: UUID) -> Profile | None:
        for profile in self.profiles:
            if profile.id != profile_id:
                continue
            return profile
    
    async def update_profile(self, profile: Profile) -> None:
        for profile in self.profiles:
            if profile.id != profile.id:
                continue
            self.profiles.remove(profile)
            self.profiles.append(profile)
            break

