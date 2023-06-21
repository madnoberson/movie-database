from typing import Optional

from pydantic import BaseModel


class AuthResponseSchema(BaseModel):

    access_token: Optional[str]
    refresh_token: Optional[str]
    token_type: str = "Bearer"