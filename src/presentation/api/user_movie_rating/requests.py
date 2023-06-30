from uuid import UUID

from pydantic import BaseModel, validator, ValidationError


class RateMovieSchema(BaseModel):
    
    movie_id: UUID
    rating: float

    @validator("rating")
    def validate_rating(cls, value: float):
        is_valid = (
            0 < value <= 10 and
            value % 0.5 == 0
        )
        if not is_valid:
            raise ValidationError
        
        return value


class ReevaluateMovieSchema(BaseModel):

    movie_id: UUID
    new_rating: float

    @validator("new_rating")
    def validate_new_rating(cls, value: float):
        is_valid = (
            0 < value <= 10 and
            value % 0.5 == 0
        )
        if not is_valid:
            raise ValidationError
        
        return value

