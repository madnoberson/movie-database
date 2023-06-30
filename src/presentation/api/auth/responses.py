from pydantic import BaseModel


class UsernameAlreadyExistsErrorSchema(BaseModel):

    username: str


class UsernameDoesNotExistErrorSchema(BaseModel):

    username: str


class IncorrectPasswordErrorSchema(BaseModel):

    message: str