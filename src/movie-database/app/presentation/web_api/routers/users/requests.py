from pydantic import BaseModel


class ChangeUsernameSchema(BaseModel):

    username: str