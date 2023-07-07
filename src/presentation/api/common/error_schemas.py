from pydantic import BaseModel


class BaseErrorSchema(BaseModel):

    message: str

