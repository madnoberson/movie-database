from pydantic import BaseModel


class ChangeUsername(BaseModel):

    username: str