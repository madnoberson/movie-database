from datetime import datetime

from app.domain.models.movies_rating_policy import MoviesRatingPolicy
from app.domain.models.user import User


class MovieRatingService:

    def check_user_can_fully_rate_movie(
        self, user: User,
        movies_rating_policy: MoviesRatingPolicy
    ) -> bool:
        if (
            user.rated_movie_count <
            movies_rating_policy.required_rated_movie_count
            or
            datetime.utcnow() - user.created_at <
            movies_rating_policy.required_days_pass_after_registration
        ):
            return False
        return True