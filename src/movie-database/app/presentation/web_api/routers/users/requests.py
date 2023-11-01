from pydantic import BaseModel


class ChangeUsernameSchema(BaseModel):

    username: str


class ChangePasswordSchema(BaseModel):
    
    old_password: str
    new_password: str