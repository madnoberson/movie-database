from pydantic import BaseModel


class UsernameAlreadyExistsErrorSchema(BaseModel):

    username: str