from pydantic import BaseModel


class UsernameAlreadyExistsErrorSchema(BaseModel):

    username: str


class UsernameDoesNotExistErrorSchema(BaseModel):

    username: str


class IncorrectPasswordErrorSchema(BaseModel):

    message: str


def get_register_responses() -> dict:
    return {
        409: {"model": UsernameAlreadyExistsErrorSchema}
    }


def get_login_responses() -> dict:
    return {
        404: {"model": UsernameDoesNotExistErrorSchema},
        401: {"model": IncorrectPasswordErrorSchema}
    }
    
