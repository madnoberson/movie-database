from pydantic import BaseModel


class RegisterSchema(BaseModel):

    username: str
    password: str