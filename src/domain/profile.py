from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True)
class Profile:

    id: UUID
    user_id: UUID
    rated_movies: int
    rated_series: int
    reviews: int
    followers: int
    following: int
    favourites: int

    @classmethod
    def create(cls, profile_id: UUID, user_id: UUID) -> "Profile":
        return Profile(
            id=profile_id, user_id=user_id, rated_movies=0, rated_series=0,
            reviews=0, followers=0, following=0, favourites=0
        )
    
