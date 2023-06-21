from pydantic import BaseModel


class UsernameAlreadyExistsErrorSchema(BaseModel):

    username: str


class UsernameDoesNotExistErrorSchemas(BaseModel):

    username: str
