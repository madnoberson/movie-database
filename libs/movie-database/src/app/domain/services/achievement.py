from app.domain.models.user import User
from app.domain.models.achievement import AchievementTypeEnum
from app.domain.policies import RatedMoviesAchievementsPolicy


class AchievementService:

    def get_rated_movie_achievement_type(
        self,
        user: User,
        rated_movies_achievements_policy: RatedMoviesAchievementsPolicy
    ) -> AchievementTypeEnum | None:
        if (
            user.rated_movie_count ==
            rated_movies_achievements_policy.rank_1.rated_movie_count
        ):
            return AchievementTypeEnum.MOVIES_RATED_1
        elif (
            user.rated_movie_count ==
            rated_movies_achievements_policy.rank_2.rated_movie_count
        ):
            return AchievementTypeEnum.MOVIES_RATED_2
        elif (
            user.rated_movie_count ==
            rated_movies_achievements_policy.rank_3.rated_movie_count
        ):
            return AchievementTypeEnum.MOVIES_RATED_3
        elif (
            user.rated_movie_count ==
            rated_movies_achievements_policy.rank_4.rated_movie_count
        ):
            return AchievementTypeEnum.MOVIES_RATED_4
        

        