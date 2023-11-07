from datetime import timedelta

from asyncpg.connection import Connection

from app.domain.policies import MoviesRatingPolicy
from app.application.common.interfaces.repositories import MoviesRatingPolicyRepository
from app.infrastructure.database.mappers import as_domain_model


class MoviesRatingPolicyRepositoryImpl(MoviesRatingPolicyRepository):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def get_movies_rating_policy(self) -> MoviesRatingPolicy:
        data = await self.connection.fetchrow(
            "SELECT mrp.* FROM movies_rating_policy mrp LIMIT 1"
        )
        
        data = dict(data)
        data["required_days_pass_after_registration"] = (
            timedelta(days=data["required_days_pass_after_registration"])
        )
        
        return as_domain_model(MoviesRatingPolicy, data)