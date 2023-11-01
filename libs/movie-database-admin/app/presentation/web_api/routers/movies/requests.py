from pydantic import BaseModel


class CreateMovieSchema(BaseModel):

    en_name: str