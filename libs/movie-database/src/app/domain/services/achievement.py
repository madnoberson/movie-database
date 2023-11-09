from app.domain.models.user import User
from app.domain.models.achievement import AchievementTypeEnum
from app.domain.policies import FilmophileAchievementsPolicy


class AchievementService:

    def get_filmophile_achievement_type(
        self,
        user: User,
        filmophile_achievements_policy: FilmophileAchievementsPolicy
    ) -> AchievementTypeEnum | None:
        if (
            user.rated_movie_count ==
            filmophile_achievements_policy.rank_1.rated_movie_count
        ):
            return AchievementTypeEnum.FILMOPHILE_1
        elif (
            user.rated_movie_count ==
            filmophile_achievements_policy.rank_2.rated_movie_count
        ):
            return AchievementTypeEnum.FILMOPHILE_2
        elif (
            user.rated_movie_count ==
            filmophile_achievements_policy.rank_3.rated_movie_count
        ):
            return AchievementTypeEnum.FILMOPHILE_3
        elif (
            user.rated_movie_count ==
            filmophile_achievements_policy.rank_4.rated_movie_count
        ):
            return AchievementTypeEnum.FILMPPHILE_4
        

        