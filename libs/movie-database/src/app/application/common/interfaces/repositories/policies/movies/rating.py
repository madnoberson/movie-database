from abc import ABC, abstractmethod

from app.domain.policies import MoviesRatingPolicy


class MoviesRatingPolicyRepository(ABC):

    @abstractmethod
    async def get_movies_rating_policy(self) -> MoviesRatingPolicy:
        raise NotImplementedError