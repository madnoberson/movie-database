from pydantic import BaseModel, Field, field_validator


class RateMovieSchema(BaseModel):

    rating: float = Field(ge=0.5, le=10)

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rating: float) -> float:
        if rating % 0.5 != 0:
            raise ValueError()
        return rating


class RerateMovieSchema(BaseModel):

    rating: float = Field(ge=0.5, le=10)

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, rating: float) -> float:
        if rating % 0.5 != 0:
            raise ValueError()
        return rating
