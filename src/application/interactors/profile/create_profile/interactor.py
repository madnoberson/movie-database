from dataclasses import dataclass
from uuid import uuid4

from src.domain.profile import Profile
from . import dto
from . import exceptions
from . import interfaces


@dataclass(frozen=True, slots=True)
class CreateProfile:

    db_gateway: interfaces.DatabaseGateway

    async def __call__(self, data: dto.CreateProfileDTO) -> dto.CreateProfileResultDTO:
        # 1.Ensure user exists
        user_exists = await self.db_gateway.check_user_exists(user_id=data.user_id)
        if not user_exists:
            raise exceptions.UserDoesNotExistError()
        
        # 2.Ensure profile doesn't exist
        profile_exists = await self.db_gateway.check_profile_exists(
            username=data.username
        )
        if profile_exists:
            raise exceptions.ProfileAlreadyExistsError()
        
        # 3.Create profile
        profile = Profile.create(
            profile_id=uuid4(), user_id=data.user_id, username=data.username
        )

        # 4.Save profile
        await self.db_gateway.save_profile(profile)
        await self.db_gateway.commit()

        return dto.CreateProfileResultDTO(profile_id=profile.id)